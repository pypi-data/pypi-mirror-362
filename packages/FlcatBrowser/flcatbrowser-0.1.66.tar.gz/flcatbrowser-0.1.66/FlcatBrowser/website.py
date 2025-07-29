from abc import ABC, abstractmethod
from enum import Enum
import json
import queue
import threading
from typing import Any, Callable, Dict, Iterable, Optional, Set

from .utils.url import extract_domain, extract_url_without_scheme

from ._js.base_requests import get_mix_js
from .enum import ListenEventType
from .utils.common import timeout_while_loop
from .exception import TaskError, TimeoutError
from .browser import BaseBrowser
class ListenContext:
    """
    用于存储一次监听的上下文信息。
    """
    def __init__(
        self,
        type_or_ids: Set[Any],
        validation_callback: Optional[Callable[[Enum, dict], bool]] = None
    ):
        # 本层要监听的事件类型集合
        self.type_or_ids = type_or_ids
        # 本层已收到的事件数据
        self.received_data: Dict[Enum, dict] = {}
        # 当前监听是否已完成（全部事件已触发）
        self.events_all_triggered = False
        # 验证回调
        self.validation_callback = validation_callback
        # 用于阻塞/唤醒本层 _wait_listen_event 的线程
        self._event = threading.Event()

class BaseWebsite(ABC):
    def __init__(self, browser: "BaseBrowser", base_url: str, listen_paths=None):
        self.browser = browser
        if listen_paths is None:
            listen_paths = []
        self.listen_paths = listen_paths
        # 线程安全的监听事件队列
        self.listen_event_queue = queue.Queue()
        # 用于多线程并发安全
        self._lock = threading.Lock()
        # 维护一个栈，用于支持多层嵌套监听
        self._contexts: list[ListenContext] = []
        # 网站根目录
        self.base_url = base_url
    
    def open_base_url(self):
        self.browser.tab.get(self.base_url)
        
    def start_listen_event(
        self,
        type_or_ids: Iterable[Any],
        validation_callback: Optional[Callable[[Any, dict], bool]] = None
    ):
        """
        在一个线程里调用，用于开始监听一批事件。允许多次、嵌套调用。
        每一次调用都会在栈顶新增一个独立的“监听上下文”。
        """
        with self._lock:
            ctx = ListenContext(
                type_or_ids=set(type_or_ids),
                validation_callback=validation_callback
            )
            self._contexts.append(ctx)

    def _wait_listen_event(self, timeout: float = 10, validation_callback=None) -> dict:
        """
        在另一个线程里调用，阻塞等待「栈顶上下文」的所有事件都触发。
        若在本函数调用之前就已触发完毕，则无需继续等待。
        
        :param timeout: 超时时间（秒），None 表示无限等待
        :param validation_callback: 若需要对栈顶已有的事件数据进行再次验证，可以传入
        :return: 成功触发的事件数据 dict (键是事件类型，值是事件内容)
        :raises TimeoutError: 若在超时时间内等待失败，则抛异常
        """
        with self._lock:
            if not self._contexts:
                # 如果连一个监听上下文都没有，则直接返回空
                return {}
            current_ctx = self._contexts[-1]

            # 如果已经全部触发，就直接返回
            if current_ctx.events_all_triggered:
                return current_ctx.received_data

            # 如果传入了新的验证回调，对当前收到的数据再过滤
            if validation_callback:
                invalid_keys = []
                for et, d in current_ctx.received_data.items():
                    if not validation_callback(et, d):
                        invalid_keys.append(et)
                # 将不符合的新验证的数据剔除
                for k in invalid_keys:
                    del current_ctx.received_data[k]

                # 验证后发现已经收到了所有事件，也无需等待
                if len(current_ctx.received_data) == len(current_ctx.type_or_ids):
                    current_ctx.events_all_triggered = True
                    return current_ctx.received_data

        # 如果还没有全部触发，则等待
        triggered = current_ctx._event.wait(timeout=timeout)
        with self._lock:
            # 再次检查一下（可能刚好超时的一刻事件才触发完）
            if not triggered and not current_ctx.events_all_triggered:
                raise TimeoutError("等待监听事件超时")

            return current_ctx.received_data
        
    def wait_listen_event_and_pop(
        self,
        timeout: float = 10, 
        validation_callback=None,
    ) -> dict:
        """
        等待栈顶上下文触发完毕后，再自动 _pop_context()。
        """
        try:
            data = self._wait_listen_event(timeout=timeout, validation_callback=validation_callback)
            self._pop_context()
            return data
        except Exception as e:
            self._pop_context()
            raise e

    def handle_listen_event(self, type_or_id, data: dict):
        """
        可能在任意线程调用。用于向“栈顶上下文”上报一个事件。
        """
        with self._lock:
            if not self._contexts:
                # 不在监听任何东西，直接返回
                return

            current_ctx = self._contexts[-1]

            # 不关心这个事件类型，直接返回
            if type_or_id not in current_ctx.type_or_ids:
                return

            # 若有验证函数，但验证不通过，则忽略
            if current_ctx.validation_callback and not current_ctx.validation_callback(type_or_id, data):
                return

            # 记录事件数据
            current_ctx.received_data[type_or_id] = data

            # 若已经收齐所有事件
            if len(current_ctx.received_data) == len(current_ctx.type_or_ids):
                current_ctx.events_all_triggered = True
                current_ctx._event.set()
        
    def enqueue_listen_event(self, event_type: Enum, data: dict):
        """
        将事件加入监听事件队列。
        :param event_type: 事件类型
        :param data: 事件数据
        """
        self.listen_event_queue.put({"event_type": event_type, "data": data})

    def wait_and_dequeue_listen_event(self):
        """
        从监听事件队列中取出事件。
        :return: 一个字典，包含事件类型和事件数据，如果队列为空，返回 None。
        """
        try:
            listen_event = self.listen_event_queue.get()
            return listen_event["event_type"] , listen_event["data"]
        except queue.Empty:
            return None

    def process_request(
        self,
        script: str,
        request_name,
        task_id,
        *args,
        auto_verify=True,
        timeout=None,
        check_mode: str = "domain"
    ):
        """
        执行请求并处理结果。
        
        :param script: 要执行的脚本路径, 务必参照js_example格式书写
        :param request_name: 请求名称，用于标识请求
        :param task_id: 任务 ID，用于监听该请求的完成事件
        :param args: 传递给脚本的额外参数
        :param auto_verify: 是否启用自动验证，目前可以自动过5秒盾
        :param timeout: 请求的超时时间（秒），默认为 None 表示不设置超时
        :param check_mode: URL 检查模式，可取 "none" / "domain" / "domain_and_path"
        :return: 请求响应结果（包含 code、message 和 data）
        :raises TaskError: 请求失败（如 HTTP 状态码不为 200 或 Cloudflare 拦截）时抛出异常
        """
        # 1. 校验 check_mode 参数
        valid_modes = {"none", "domain", "domain_and_path"}
        if check_mode not in valid_modes:
            raise ValueError(f"不支持的检查模式: {check_mode}, 仅支持: {valid_modes}")

        # 2. 根据 check_mode 进行不同的 URL 检查
        if check_mode == "none":
            # 不做任何检查
            pass
        elif check_mode == "domain":
            # 只检查域名是否一致
            if extract_domain(self.browser.tab.url) != extract_domain(self.base_url):
                self.browser.tab.get(self.base_url)
        elif check_mode == "domain_and_path":
            # 检查域名 + 路径
            if extract_url_without_scheme(self.browser.tab.url) != extract_url_without_scheme(self.base_url):
                self.browser.tab.get(self.base_url)

        # 如果遇到验证则通过验证后重试请求
        for i in range(2):
            self.start_listen_event([task_id])
            self.browser.tab.run_js_loaded(get_mix_js(script), request_name, task_id, *args, timeout=timeout)
            res = self.wait_listen_event_and_pop(timeout)[task_id]
            http_code = res.get('code')
            http_message = res.get('message')
            http_data = res.get('data', "")
            if auto_verify:
                # 处理cf
                if http_code == 403 and "Just a moment..." in http_data:
                    old_cf_clearance = self.browser.tab.cookies().as_dict().get('cf_clearance')
                    self.browser.tab.get(self.base_url)
                    timeout_while_loop(lambda ctx, o_cf_clearance = old_cf_clearance: self.browser.tab.cookies().as_dict().get('cf_clearance') == o_cf_clearance, None, {}, 1*30, 2)
                    # 如果第二次还是出现cf验证则报错
                    if i == 1:
                        raise TaskError('403', code = http_code)
                else:
                    break
            else:
                break

        if not (200 <= http_code < 300):
            raise TaskError(http_message , code = http_code)
        return res
    
    def listen_console_callback(self, response):
        """进行控制台监听"""
        try:
            body = json.loads(response.text)
        except Exception:
            return
        if not isinstance(body, dict):
            return
        data = body.get('data', {})
        if body.get('type') == ListenEventType.REQUEST.value:
            request_id = body.get('id')
            self.handle_listen_event(request_id, data)

    def listen_path_callback(self, response):
        """进行请求监听"""
        pass

    def _pop_context(self) -> Optional[ListenContext]:
        """
        若上一层调用者需要在“监听结束后”弹栈，可调用此方法。
        也可在 _wait_listen_event 返回后，手动调用本方法来清理栈顶。
        
        :return: 刚被弹出的 ListenContext；若栈为空返回 None
        """
        with self._lock:
            if self._contexts:
                return self._contexts.pop()
            return None