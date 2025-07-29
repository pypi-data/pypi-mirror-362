from urllib.parse import urlparse, urlunparse

def extract_domain(url):
    """
    从URL中提取域名部分。

    参数:
    url (str): 需要提取的URL。

    返回:
    str: 提取的域名。
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

def extract_url_without_scheme(url):
    """
    提取URL中除了协议（scheme）之外的所有部分。

    参数:
    url (str): 需要提取的URL。

    返回:
    str: 去掉协议的URL。
    """
    parsed_url = urlparse(url)
    # 将 scheme 设置为空字符串
    url_without_scheme = urlunparse(('', parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    return url_without_scheme