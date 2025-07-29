import time


def timeout_while_loop(condition_func=None, action_func=None, context: dict={}, timeout: int = 10, poll_interval=0.1):
    """
    带超时时间的while循环，支持上下文变量传入，并通过action_func的返回值控制退出循环。

    参数:
        timeout (float): 超时时间（单位：秒）。
        condition_func (function): 可选，判断循环是否继续的函数，接收 context 作为参数。
        action_func (function): 可选，每次循环执行的函数，接收 context 作为参数，返回 False 表示退出循环。
        poll_interval (float): 每次检查条件的间隔时间，默认 0.1 秒。
        context (dict): 上下文字典，用于传递和共享外部变量。

    返回:
        None

    异常:
        TimeoutError: 如果超过指定的超时时间未退出循环，则抛出此异常。
    """
    start_time = time.time()

    while (condition_func is None or condition_func(context)):
        # 检查是否超时
        if time.time() - start_time > timeout:
            raise TimeoutError("While 循环执行超时！")

        # 执行指定操作，返回 False 表示退出循环
        if action_func:
            should_continue = action_func(context)
            if should_continue is False:
                break

        # 等待一小段时间再检查条件，减少CPU占用
        time.sleep(poll_interval)