import socket

def is_port_in_use(port):
    """
    检查指定端口是否正在使用，支持跨平台。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return False  # 端口未被占用
        except OSError:
            return True  # 端口已被占用

def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 绑定到一个随机的端口
            s.bind(('', 0))
            # 获取分配的端口
            port = s.getsockname()[1]
        return port