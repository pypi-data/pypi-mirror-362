import traceback
class TaskError(Exception):
    """
    自定义异常类，用于处理任务相关的异常。
    """

    def __init__(
        self,
        message: str,
        data: dict | None = None,
        code: int = None,
        original_exception: Exception | None = None,
    ) -> None:
        """
        初始化 TaskError 异常。

        :param message: 异常的消息内容。
        :param data: 可选的附加数据，默认为 None。
        :param code: 错误码，默认为 500。
        :param original_exception: 可选的原始异常对象。
        """
        self.message: str = message
        self.data: dict = data or {}
        self.code: int = code or 500
        self.original_exception: Exception | None = original_exception

        # 记录当前抛出 TaskError 时的调用栈（不包含原始异常）
        self.current_stack_str = "".join(traceback.format_stack())

        if original_exception is not None:
            original_exc_list = traceback.format_exception(
                type(original_exception),
                original_exception,
                original_exception.__traceback__
            )
            self.original_stack_str = "".join(original_exc_list)
        else:
            self.original_stack_str = ""

        super().__init__(self.message)

    def __str__(self) -> str:
        """
        返回异常的字符串表示形式（附带当前栈和原始栈）。
        """
        base_message = f"[{self.code}] {self.message}"
        context_message = f"Data: {self.data}" if self.data else "No additional data"

        if not self.original_exception:
            # 无原始异常，只返回当前异常信息和当前调用栈
            return (
                f"{base_message}\n"
                f"{context_message}\n\n"
                f"=== Current Stack ===\n"
                f"{self.current_stack_str}"
            )

        # 存在原始异常时，既包含当前 TaskError 抛出位置的调用栈，也包含原始异常栈
        return (
            f"{base_message}\n"
            f"{context_message}\n\n"
        )
    
class TimeoutError(Exception):
    """自定义超时异常"""
    pass

class ElementNotInViewportError(Exception):
    """自定义元素不在视窗内，需要滚动窗口"""
    pass

class NotImplementError(Exception):
    """尚未实现"""
    pass

class NotSupportError(Exception):
    """不支持"""
    pass

class RequestParameterError(Exception):
    """请求参数错误"""
    pass

class CookieExpiredError(Exception):
    """Cookie过期"""
    pass

class InternalError(Exception):
    pass

class HTTPError(Exception):
    """HTTP请求错误"""

    def __init__(self, code: int, message: str) -> None:
        """
        初始化 HTTPError 异常。

        :param code: HTTP 状态码。
        :param message: 错误消息。
        """
        self.code: int = code
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        返回异常的字符串表示形式。

        :return: 格式化的 HTTP 错误信息字符串。
        """
        return f"HttpCode: {self.code}\nMessage: {self.message}"
    
