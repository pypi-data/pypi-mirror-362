import random

from DrissionPage import Chromium

from .ua import UserAgentManager

from .finger_print import FingerPrint

def generate_random_device_info(user_agent: str) -> dict:
    """
    根据传入的 user_agent，在合理范围内随机生成其它指纹信息并返回。
    返回数据结构示例：
    {
        "cpu_core": 4,
        "timezone": "Europe/London",
        "latitude": 51.5074,
        "longitude": -0.1276,
        "user_agent": "传入或随机生成的UA",
        "platform": "iPhone",
        "accept_language": "en-GB",
        "disable_cookies": False,
        "touch_mode": {
            "enabled": True,
            "max_touch_points": 16
        },
        "screen_size": {
            "width": 360,
            "height": 740,
            "mobile": True,
            "scale": 1.1
        }
    }
    """
    # ---- 一些示例常量池（实际可根据自己收集的真实数据来扩充） ----

    # 1) 不同操作系统常见的屏幕分辨率范围（手机/PC）
    ios_screen_options = [
        {"width": 375, "height": 667, "scale": 2},   # iPhone 8
        {"width": 375, "height": 812, "scale": 3},   # iPhone X / XS
        {"width": 414, "height": 896, "scale": 3},   # iPhone XR / 11
        {"width": 390, "height": 844, "scale": 3},   # iPhone 12
    ]
    android_screen_options = [
        {"width": 360, "height": 640, "scale": 2},   # 较常见
        {"width": 412, "height": 732, "scale": 2.5}, # Pixel 3 XL等
        {"width": 360, "height": 780, "scale": 3},   # 一些大屏机
    ]
    windows_screen_options = [
        {"width": 1366, "height": 768, "scale": 1},
        {"width": 1920, "height": 1080, "scale": 1},
        {"width": 1600, "height": 900, "scale": 1},
    ]
    mac_screen_options = [
        {"width": 1440, "height": 900,  "scale": 2},  # Retina MBP 13"
        {"width": 1680, "height": 1050, "scale": 2},  # MBP 15" (部分型号)
        {"width": 1280, "height": 800,  "scale": 2},  # MBA 等
    ]

    # 2) 不同类型设备常见的 CPU 核心数范围
    ios_cpu_options = [2, 4, 6]
    android_cpu_options = [4, 6, 8]
    windows_cpu_options = [2, 4, 6, 8, 16]
    mac_cpu_options = [2, 4, 6, 8, 10]

    # 3) 不同语种的 Accept-Language 可做更多扩展
    language_options = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.9",
        "zh-CN,zh;q=0.9",
        "fr-FR,fr;q=0.9"
    ]

    # 4) 一些常见时区（此处仅示例，可自行扩充）
    timezone_options = [
        "Europe/London",
        "Asia/Shanghai",
        "America/Los_Angeles",
        "America/New_York",
        "Asia/Tokyo",
        "Europe/Berlin"
    ]

    # 5) 针对常见时区的经纬度可做更多精细映射；此处示例仅简单随机
    latlong_options = [
        (51.5074, -0.1276),    # London
        (31.2304, 121.4737),   # Shanghai
        (34.0522, -118.2437),  # Los Angeles
        (40.7128, -74.0060),   # New York
        (35.6895, 139.6917),   # Tokyo
        (52.5200, 13.4050)     # Berlin
    ]

    # ---- 根据UA初步判断设备类型 ----
    ua_lower = user_agent.lower()

    if "iphone" in ua_lower:
        device_type = "iOS"
        platform = "iPhone"
        cpu_cores = random.choice(ios_cpu_options)
        screen_choice = random.choice(ios_screen_options)
        is_mobile = True
        touch_enabled = True
    elif "android" in ua_lower:
        device_type = "Android"
        platform = "Android"
        cpu_cores = random.choice(android_cpu_options)
        screen_choice = random.choice(android_screen_options)
        is_mobile = True
        touch_enabled = True
    elif "windows nt" in ua_lower:
        device_type = "Windows"
        platform = "Win32"  # 也可根据 user_agent 是否包含 'Win64' 动态判断
        cpu_cores = random.choice(windows_cpu_options)
        screen_choice = random.choice(windows_screen_options)
        is_mobile = False
        touch_enabled = False
    elif "macintosh" in ua_lower:
        device_type = "Mac"
        platform = "MacIntel"  # 或 "Mac OS X"
        cpu_cores = random.choice(mac_cpu_options)
        screen_choice = random.choice(mac_screen_options)
        is_mobile = False
        touch_enabled = False
    else:
        # 如果都没匹配，默认按 PC 处理
        device_type = "OtherPC"
        platform = "Win32"
        cpu_cores = random.choice(windows_cpu_options)
        screen_choice = random.choice(windows_screen_options)
        is_mobile = False
        touch_enabled = False

    # ---- 组合生成最终 fingerprint 字典 ----

    # 随机选择时区、地理位置（示例根据同一个索引来保证经纬度与对应时区相匹配，或也可完全乱序）
    tz_index = random.randrange(len(timezone_options))
    chosen_tz = timezone_options[tz_index]
    chosen_lat, chosen_lon = latlong_options[tz_index]

    real_device = {
        "cpu_core": cpu_cores,
        "timezone": chosen_tz,
        "latitude": chosen_lat,
        "longitude": chosen_lon,
        # 这里的 UA 直接返回传入的；如需随机生成别的 UA，可在此处替换
        "user_agent": user_agent,
        "platform": platform,
        "accept_language": random.choice(language_options),
        # 随机是否禁用 cookies
        "disable_cookies": False,
        "touch_mode": {
            "enabled": touch_enabled,
            "max_touch_points": (16 if touch_enabled else 0)
        },
        "screen_size": {
            "width": screen_choice["width"],
            "height": screen_choice["height"],
            "mobile": is_mobile,
            "scale": screen_choice["scale"]
        }
    }

    return real_device

def apply_device_info(fp: FingerPrint, device_info):
    """
    将随机选出的设备信息应用到 FingerPrint 实例中。
    """
    # 设置 CPU 核心数
    if device_info.get('cpu_core'):
        fp.set_cpu_core(device_info['cpu_core'])

    # 清除 RPA 特征（自动化标记）
    fp.set_rpa_feature(enabled=False)

    # 是否禁用 Cookies
    if device_info.get('disable_cookies', False):
        fp.disable_cookies()

    # 设置时区
    if device_info.get('timezone'):
        fp.set_timezone(device_info['timezone'])

    # 设置地理位置（经纬度）
    if device_info.get('latitude') or device_info.get('longitude'):
        fp.set_set_geolocation(latitude=device_info['latitude'],
                            longitude=device_info['longitude'])
    
    if device_info.get('accept_language'):
        fp.set_locale(locale=device_info['accept_language'])

    # 设置 User-Agent、平台和语言
    if device_info.get('user_agent'):
        fp.set_user_agent(
            user_agent=device_info['user_agent'],
            platform=device_info['platform'],
            accept_language=device_info['accept_language']
        )

    # 设置触摸模式
    if device_info.get('touch_mode'):
        fp.set_touch_mode(
            enabled=device_info['touch_mode']['enabled'],
            max_touch_points=device_info['touch_mode']['max_touch_points']
        )

    # 设置屏幕尺寸及移动/缩放信息
    if device_info.get('screen_size'):
        fp.set_size(
            width=device_info['screen_size']['width'],
            height=device_info['screen_size']['height'],
            mobile=device_info['screen_size']['mobile'],
            scale=device_info['screen_size']['scale']
        )

# ------------------ 以下为简单演示用例 ------------------
if __name__ == "__main__":
    # 创建浏览器对象
    browser = Chromium()

    # 获取当前活动 Tab
    tab = browser.latest_tab

    # 创建 FingerPrint 对象
    fp = FingerPrint(tab)

    manager = UserAgentManager()

    # 这里可以做“批量处理”，例如循环多次，每次都随机切换一个指纹进行访问
    for i in range(10):  # 示例：循环 5 次
        device_info = generate_random_device_info(manager.get_random_user_agent(keep_time=5))
        apply_device_info(fp, device_info)

        # 访问目标网站（以 ip77.net 测试为例）
        tab.get("https://ip77.net/")
        print(f"第{i+1}次访问 - 页面标题：{tab.title}")

        # 在实际业务中，可以在这一步执行更多的操作或验证逻辑
        # ...

        input("按下回车键继续下一个随机指纹测试...")

    # 退出时记得关闭浏览器
    browser.quit()