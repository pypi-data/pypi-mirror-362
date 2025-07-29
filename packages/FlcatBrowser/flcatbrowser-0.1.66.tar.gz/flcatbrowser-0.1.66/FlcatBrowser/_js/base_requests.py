import os

def _get_current_function_path():
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(current_file_path)
    return current_dir

def _read_file_to_string(file_path):
    """
    从指定路径读取文件内容并返回为字符串。

    :param file_path: 文件的完整路径
    :return: 文件内容的字符串表示
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content

def get_mix_js(custom_js_path):
    base_js= _read_file_to_string(os.path.join(_get_current_function_path(),"base_request.js"))
    custom_js = _read_file_to_string(custom_js_path)

    return custom_js + base_js