import asyncio
import queue
import random
import threading
import time
from typing import Any, Callable, Optional

import loguru

class QueueFullError(Exception):
    """队列已满异常

    当任务队列达到最大容量，无法接受更多任务时抛出此异常。

    :param message: 异常的消息字符串。
    :param max_size: 队列的最大容量。
    """
    def __init__(self, message: str = "任务队列已满，无法提交新任务。", max_size: int | None = None) -> None:
        """
        初始化 QueueFullError 异常。

        :param message: 异常的消息内容，默认提示队列已满。
        :param max_size: 可选的队列最大容量。
        """
        self.message: str = message
        self.max_size: int | None = max_size
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        返回异常的字符串表示形式。

        :return: 格式化的队列已满异常信息字符串。
        """
        if self.max_size is not None:
            return f"{self.message} 队列最大容量为: {self.max_size}."
        return self.message

class Task:
    """
    表示一个需要执行的任务
    """
    def __init__(
        self,
        func: Callable[..., Any],
        args: tuple = (),
        kwargs: dict = None,
        retry: int = 3,
        timeout: float = 5.0,
    ):
        """
        :param func: 任务函数
        :param args: 函数位置参数
        :param kwargs: 函数关键字参数
        :param retry: 最大重试次数
        :param timeout: 超时时间（秒）
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs if kwargs is not None else {}
        self.retry = retry
        self.timeout = timeout

        # 任务执行结果以及状态
        self.result = None
        self.exception = None
        self.finished = threading.Event()

    def run(self, worker: "Worker" = None) -> None:
        """
        执行任务，并支持超时/异常处理。
        新增 worker 参数，用于在任务函数中访问当前执行该任务的 Worker。
        """
        try:
            # 调用用户自定义的任务函数时，将 self（Task对象）和 worker 都传入
            self.result = self.func(self, worker, *self.args, **self.kwargs)
            self.exception = None
        except Exception as e:
            self.exception = e

    def wait(self, timeout: Optional[float] = None) -> Any:
        """
        等待任务执行结束，可指定等待时间。
        如果没有超时，返回执行结果或者抛出异常。
        """
        # 如果没有传入超时时间使用任务超时时间
        if not timeout:
            timeout = self.timeout
        finished_in_time = self.finished.wait(timeout=timeout)
        if not finished_in_time:
            raise TimeoutError("Wait for task result timed out")

        # 如果任务执行抛出异常，这里可以再次向上层抛出
        if self.exception is not None:
            raise self.exception
        return self.result

    async def wait_async(self, timeout: Optional[float] = None) -> Any:
        """
        等待任务执行结束，非阻塞方式，支持 asyncio。
        如果没有超时，返回执行结果或者抛出异常。
        """
        try:
            loop = asyncio.get_event_loop()
            # 将线程的 Event 转换为 asyncio 的 Future
            await asyncio.wait_for(loop.run_in_executor(None, self.finished.wait), timeout=timeout)

            # 如果任务执行抛出异常，这里可以再次向上层抛出
            if self.exception is not None:
                raise self.exception
            return self.result
        except asyncio.TimeoutError:
            raise TimeoutError("Wait for task result timed out")

class Worker(threading.Thread):
    """
    工作线程，不断从队列中取出任务执行
    """
    def __init__(self, task_queue: "TaskQueue", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_queue = task_queue
        self.daemon = True

    def run(self) -> None:
        while True:
            task = self.task_queue.queue.get(block=True)
            if task is None:
                self.task_queue.queue.task_done()
                break

            retries_left = task.retry

            while retries_left >= 0:
                task.run(worker=self)
                if task.exception is None:
                    # 执行成功
                    break
                else:
                    retries_left -= 1
                    if retries_left >= 0:
                        loguru.logger.exception(task.exception)
                        loguru.logger.error(
                            f"[Worker-{self.name}] Task failed, retrying... {retries_left} retries left."
                        )

            task.finished.set()

            self.task_queue.queue.task_done()

            if task.exception is not None:
                loguru.logger.error("[Worker-%s] Task completely failed after all retries:" % self.name)
                loguru.logger.exception(task.exception)


class TaskQueue:
    """
    任务队列，用于提交和管理任务
    """
    def __init__(self, num_workers: int = 2, max_size: int = 0, create_interval_time: int = None):
        self.queue = queue.Queue(maxsize=max_size)
        self.workers = []
        self._init_workers_concurrence(num_workers, create_interval_time)

    def _init_workers_concurrence(self, num_workers: int, create_interval_time: int = None) -> None:
        threads = []

        for i in range(num_workers):
            thread = threading.Thread(target=self.create_worker, args=(i,))
            threads.append(thread)
            thread.start()
            if create_interval_time:
                # 避免创建资源过快
                time.sleep(create_interval_time)

        for thread in threads:
            thread.join()  # 等待所有线程完成

    def create_worker(self, index):
            worker = Worker(self, name=f"Worker-{index + 1}")
            worker.start()
            self.workers.append(worker)

    def submit(
        self,
        func: Callable[..., Any],
        args: tuple = (),
        kwargs: dict = None,
        retry: int = 3,
        timeout: float = None,
    ) -> Task:
        """
        向任务队列提交一个任务，并返回封装的 Task 对象

        :param timeout: 任务超时时间，等价于wait中的timeout
        """
        task = Task(func, args, kwargs, retry, timeout)
        try:
            # 非阻塞模式 put，如果队列满了会抛出 queue.Full
            self.queue.put(task, block=False)
            return task
        except queue.Full:
            raise QueueFullError("[TaskQueue] 队列已满，无法提交新任务。",self.queue.maxsize)

    def shutdown(self, wait: bool = True):
        """
        关闭线程池，发送结束信号
        :param wait: 是否等待所有任务完成后再返回
        """
        # 向队列中放入 N 个 None，让所有 Worker 线程停止
        for _ in self.workers:
            self.queue.put(None)

        if wait:
            self.queue.join()

        for w in self.workers:
            w.join()


# def first_fail_second_success_task(task_obj, worker_obj):
#     """
#     第一次执行失败，第二次执行成功的任务
#     """
#     if not hasattr(task_obj, 'has_failed'):
#         task_obj.has_failed = True
#         print(f"[{worker_obj.name}] 第一次执行失败")
#         raise ValueError("模拟第一次执行失败")
#     else:
#         print(f"[{worker_obj.name}] 第二次执行成功")
#         return "成功"

# # ========== 测试示例修改 ==========
# if __name__ == "__main__":
#     # 创建任务队列
#     tq = TaskQueue(num_workers=2)

#     # 提交第一次失败，第二次成功的任务
#     fail_then_success_task = tq.submit(func=first_fail_second_success_task, retry=2, timeout=3)

#     # 等待并获取结果
#     try:
#         result = fail_then_success_task.wait()
#         print(f"[Main] 第一次失败，第二次成功任务结果: {result}")
#     except Exception as e:
#         print(f"[Main] 任务失败: {e}")

#     # 优雅关闭队列
#     tq.shutdown(wait=True)
#     print("[Main] 所有任务已完成，队列已关闭。")

# ========== 测试示例 ==========
if __name__ == "__main__":

    def my_task(task_obj, worker_obj, x, y):
        """
        任务函数示例：
        - task_obj: 当前任务的 Task 实例
        - worker_obj: 正在执行该任务的 Worker 实例
        - x, y: 具体业务参数
        """
        print(f"[{worker_obj.name}] Executing my_task with x={x}, y={y}")
        time.sleep(1)
        return x + y

    def error_task(task_obj, worker_obj):
        """
        用于测试错误与重试的任务函数
        """
        print(f"[{worker_obj.name}] Executing error_task (will raise error)")
        time.sleep(1)
        raise ValueError("Intentional Error")

    # 创建任务队列
    tq = TaskQueue(num_workers=2)

    # 提交几个成功任务
    tasks = []
    for i in range(3):
        t = tq.submit(func=my_task, args=(i, i + 1), retry=2, timeout=10)
        tasks.append(t)

    # 提交一个一定会报错的任务
    error_t = tq.submit(func=error_task, retry=2, timeout=10)

    # 等待并获取结果
    for i, task in enumerate(tasks):
        try:
            result = task.wait()
            print(f"[Main] Task {i} result: {result}")
        except Exception as e:
            print(f"[Main] Task {i} failed: {e}")

    # 等待并获取报错任务的结果
    try:
        error_t.wait()
    except Exception as e:
        print(f"[Main] Error task failed as expected: {e}")

    # 优雅关闭队列
    tq.shutdown(wait=True)
    print("[Main] All tasks done, queue shut down.")

# def long_running_task(task_obj, worker_obj):
#     """
#     一个执行时间较长的任务，用于测试超时功能
#     """
#     print(f"[{worker_obj.name}] 开始执行长耗时任务 (将持续 5 秒)")
#     time.sleep(5)  # 模拟 5 秒长时间执行
#     return "长耗时任务完成"

# if __name__ == "__main__":
#     # 创建任务队列
#     tq = TaskQueue(num_workers=1)

#     # 提交一个执行时间会超过 timeout 的任务
#     # 将 timeout 设置为 2 秒，任务本身需要 5 秒
#     timeout_task = tq.submit(
#         func=long_running_task,
#         retry=2,           # 不需要多次重试
#         timeout=2.0        # 超时时间设置为 2 秒
#     )

#     # 等待任务结果，如果超过 2 秒没有完成，则触发 TimeoutError
#     try:
#         result = timeout_task.wait()
#         print(f"[Main] 任务结果: {result}")
#     except TimeoutError as e:
#         print(f"[Main] 任务超时：{e}")
#     except Exception as e:
#         print(f"[Main] 任务执行时发生其它错误：{e}")

#     # 优雅关闭队列
#     tq.shutdown(wait=True)
#     print("[Main] 所有任务已完成或停止，队列已关闭。")