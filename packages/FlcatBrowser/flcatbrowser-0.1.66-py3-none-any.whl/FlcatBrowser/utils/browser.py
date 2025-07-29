import os
import loguru
import platform

def close_all_chrome():
    """
    跨平台关闭所有Chrome浏览器进程。
    Windows: taskkill /F /IM chrome.exe
    Mac/Linux: pkill -9 chrome
    """
    system_name = platform.system()
    try:
        if system_name == "Windows":
            os.system("taskkill /F /IM chrome.exe")
        elif system_name == "Darwin" or system_name == "Linux":
            os.system('pkill -9 -f "Google Chrome"')
        else:
            loguru.logger.error(f"当前系统 {system_name} 暂不支持自动关闭Chrome，请手动处理。")
    except Exception as e:
        loguru.logger.exception(f"关闭Chrome浏览器进程时出现异常：{e}")