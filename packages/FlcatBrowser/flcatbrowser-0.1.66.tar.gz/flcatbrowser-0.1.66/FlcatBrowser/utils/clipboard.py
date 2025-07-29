import platform
from typing import Tuple
import pyperclip
import win32clipboard
import win32con
import struct
import os
import io
import base64
from PIL import Image
from typing import Union, Tuple

# Windows 专用模块
if platform.system() == 'Windows':
    import win32clipboard
    import win32con

def save_clipboard():
    """保存当前剪贴板内容（Windows支持多格式，其他平台仅保存文本）"""
    system = platform.system()
    saved_data = {'system': system}

    if system == 'Windows':
        # Windows 保存所有剪贴板格式
        try:
            win32clipboard.OpenClipboard()
            formats = []
            current_format = 0
            while True:
                current_format = win32clipboard.EnumClipboardFormats(current_format)
                if current_format == 0:
                    break
                formats.append(current_format)
            
            data = {}
            for fmt in formats:
                try:
                    data[fmt] = win32clipboard.GetClipboardData(fmt)
                except Exception as e:
                    pass  # 跳过无法读取的格式
            saved_data['data'] = data
        finally:
            win32clipboard.CloseClipboard()
    else:
        # 其他平台仅保存文本
        try:
            saved_data['text'] = pyperclip.paste()
        except pyperclip.PyperclipException:
            saved_data['text'] = None
    return saved_data

def restore_clipboard(saved_data):
    """恢复剪贴板内容"""
    system = saved_data.get('system', '')
    
    if system == 'Windows' and 'data' in saved_data:
        # Windows 恢复多格式
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            for fmt, data in saved_data['data'].items():
                win32clipboard.SetClipboardData(fmt, data)
        finally:
            win32clipboard.CloseClipboard()
    else:
        # 其他平台恢复文本
        if saved_data.get('text'):
            pyperclip.copy(saved_data['text'])
            
def set_clipboard(text: str) -> Tuple[bool, str]:
    """
    设置剪贴板文本内容（跨平台）
    
    参数:
        text (str): 要设置的文本内容
        
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    try:
        # 优先使用 pyperclip 的跨平台方案
        pyperclip.copy(text)
        
        # 二次验证（Windows 专用）
        if platform.system() == "Windows":
            win32clipboard.OpenClipboard()
            clipboard_text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            if clipboard_text != text:
                raise RuntimeError("剪贴板验证失败，内容不一致")
                
        return (True, "")
        
    except Exception as e:
        error_msg = f"设置剪贴板失败: {str(e)}"
        
        # 尝试备用方案 (Windows)
        if platform.system() == "Windows":
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return (True, "")
            except Exception as win_err:
                error_msg += f" | 备用方案失败: {str(win_err)}"
        
        return (False, error_msg)



def copy_image_to_clipboard_from_binary(image_data: bytes, image_format: str = None) -> Tuple[bool, str]:
    """
    从二进制数据复制图片到剪贴板
    
    参数:
        image_data: 图片的二进制数据
        image_format: 图片格式（如 'PNG', 'JPEG' 等），如果为 None 会尝试自动检测
        
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    if platform.system() != "Windows":
        return (False, "图片复制功能仅支持 Windows 系统")
    
    try:
        # 从二进制数据创建图片对象
        image = Image.open(io.BytesIO(image_data))
        
        # 转换为 RGB 格式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 创建 BMP 格式的字节流
        output = io.BytesIO()
        image.save(output, 'BMP')
        bmp_data = output.getvalue()[14:]  # 去掉 BMP 文件头
        output.close()
        
        # 复制到剪贴板
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, bmp_data)
        win32clipboard.CloseClipboard()
        return (True, "")
    except Exception as e:
        return (False, f"从二进制数据复制图片失败: {str(e)}")

def copy_image_to_clipboard_from_base64(base64_data: str) -> Tuple[bool, str]:
    """
    从 base64 编码的数据复制图片到剪贴板
    
    参数:
        base64_data: base64 编码的图片数据（可以包含或不包含 data:image/xxx;base64, 前缀）
        
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    try:
        # 处理 data URL 格式
        if base64_data.startswith('data:'):
            # 提取 base64 部分
            base64_data = base64_data.split(',', 1)[1]
        
        # 解码 base64
        image_data = base64.b64decode(base64_data)
        
        # 使用二进制数据复制函数
        return copy_image_to_clipboard_from_binary(image_data)
    except Exception as e:
        return (False, f"从 base64 数据复制图片失败: {str(e)}")

def copy_file_to_clipboard_from_binary(file_data: bytes, filename: str, temp_dir: str = None) -> Tuple[bool, str]:
    """
    从二进制数据创建临时文件并复制到剪贴板
    
    参数:
        file_data: 文件的二进制数据
        filename: 文件名
        temp_dir: 临时目录路径，如果为 None 则使用系统临时目录
        
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    import tempfile
    
    if platform.system() != "Windows":
        return (False, "文件复制功能仅支持 Windows 系统")
    
    try:
        # 创建临时文件
        if temp_dir is None:
            temp_dir = tempfile.gettempdir()
        
        temp_path = os.path.join(temp_dir, filename)
        
        # 写入二进制数据
        with open(temp_path, 'wb') as f:
            f.write(file_data)
        
        # 复制文件路径到剪贴板
        if copy_files_to_clipboard([temp_path]):
            return (True, f"临时文件已创建: {temp_path}")
        else:
            return (False, "复制文件到剪贴板失败")
    except Exception as e:
        return (False, f"从二进制数据复制文件失败: {str(e)}")

def copy_file_to_clipboard_from_base64(base64_data: str, filename: str, temp_dir: str = None) -> Tuple[bool, str]:
    """
    从 base64 编码的数据创建文件并复制到剪贴板
    
    参数:
        base64_data: base64 编码的文件数据
        filename: 文件名
        temp_dir: 临时目录路径
        
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    try:
        # 解码 base64
        file_data = base64.b64decode(base64_data)
        
        # 使用二进制数据复制函数
        return copy_file_to_clipboard_from_binary(file_data, filename, temp_dir)
    except Exception as e:
        return (False, f"从 base64 数据复制文件失败: {str(e)}")

def set_clipboard_universal(content: Union[str, bytes], content_type: str = 'text', **kwargs) -> Tuple[bool, str]:
    """
    通用剪贴板设置函数，支持多种内容类型
    
    参数:
        content: 内容（字符串、二进制数据或 base64 字符串）
        content_type: 内容类型 ('text', 'image', 'image_base64', 'file', 'file_base64')
        **kwargs: 额外参数
            - filename: 文件名（用于 file 类型）
            - temp_dir: 临时目录（用于 file 类型）
            - image_format: 图片格式（用于 image 类型）
            
    返回:
        Tuple[bool, str]: (操作是否成功, 错误消息)
    """
    if content_type == 'text':
        return set_clipboard(content)
    
    elif content_type == 'image':
        if isinstance(content, str):
            # 文件路径
            return set_clipboard_image(content)
        elif isinstance(content, bytes):
            # 二进制数据
            return copy_image_to_clipboard_from_binary(content, kwargs.get('image_format'))
    
    elif content_type == 'image_base64':
        return copy_image_to_clipboard_from_base64(content)
    
    elif content_type == 'file':
        if isinstance(content, str):
            # 文件路径
            return (copy_files_to_clipboard([content]), "")
        elif isinstance(content, bytes):
            # 二进制数据
            filename = kwargs.get('filename', 'temp_file.bin')
            temp_dir = kwargs.get('temp_dir')
            return copy_file_to_clipboard_from_binary(content, filename, temp_dir)
    
    elif content_type == 'file_base64':
        filename = kwargs.get('filename', 'temp_file.bin')
        temp_dir = kwargs.get('temp_dir')
        return copy_file_to_clipboard_from_base64(content, filename, temp_dir)
    
    else:
        return (False, f"不支持的内容类型: {content_type}")

# 读取剪贴板中的图片为二进制数据
def get_clipboard_image_binary() -> Union[bytes, None]:
    """
    从剪贴板读取图片并返回二进制数据
    
    返回:
        bytes: 图片的二进制数据（PNG 格式），如果没有图片则返回 None
    """
    if platform.system() != "Windows":
        return None
    
    try:
        win32clipboard.OpenClipboard()
        
        # 检查是否有 DIB 格式的图片
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB):
            dib_data = win32clipboard.GetClipboardData(win32con.CF_DIB)
            
            # 将 DIB 数据转换为 PIL Image
            # DIB 数据需要添加 BMP 文件头
            bmp_header = b'BM' + struct.pack('<I', len(dib_data) + 14) + b'\x00\x00\x00\x00\x36\x00\x00\x00'
            bmp_data = bmp_header + dib_data
            
            # 转换为 PNG 格式
            image = Image.open(io.BytesIO(bmp_data))
            output = io.BytesIO()
            image.save(output, 'PNG')
            return output.getvalue()
        
        return None
    except Exception as e:
        print(f"读取剪贴板图片失败: {e}")
        return None
    finally:
        win32clipboard.CloseClipboard()

def get_clipboard_image_base64() -> Union[str, None]:
    """
    从剪贴板读取图片并返回 base64 编码
    
    返回:
        str: base64 编码的图片数据，如果没有图片则返回 None
    """
    image_data = get_clipboard_image_binary()
    if image_data:
        return base64.b64encode(image_data).decode('utf-8')
    return None

if __name__ == "__main__":
    # 测试代码
    success, message = set_clipboard_universal("Hello, World!", content_type='text')
    print(f"Text copy success: {success}, message: {message}")
    
    # 测试图片复制
    with open("C:\\Users\\82707\\Desktop\\1.png", "rb") as f:
        image_data = f.read()
    success, message = set_clipboard_universal(image_data, content_type='image')
    print(f"Image copy success: {success}, message: {message}")
    import time
    time.sleep(1)  # 等待剪贴板操作完成
    # 测试从剪贴板读取图片
    image_base64 = get_clipboard_image_base64()
    print(f"Clipboard image base64: {image_base64}")
