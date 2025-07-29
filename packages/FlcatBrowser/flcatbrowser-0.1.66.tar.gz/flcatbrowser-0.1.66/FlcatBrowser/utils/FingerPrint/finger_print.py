#!/usr/bin/env python
# -*- coding:utf-8 -*-
from DrissionPage._pages.mix_tab import MixTab

class FingerPrint:
    def __init__(self, tab: MixTab):
        self.tab = tab

    def set_timezone(self, timezone="Europe/London"):
        timezone_param = {
                "timezoneId": timezone
        }
        self.tab.run_cdp("Emulation.setTimezoneOverride", **timezone_param)
        return self

    def set_set_geolocation(self, latitude=51.5074, longitude=-0.1276, accuracy=100):
        geolocation_param = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": accuracy
        }
        self.tab.run_cdp("Emulation.setGeolocationOverride", **geolocation_param)
        return self

    def set_user_agent(self, user_agent, platform='iPhone', accept_language='en-GB'):
        ua_param = {
            "userAgent": user_agent,
            "platform": platform,
            "acceptLanguage": accept_language
        }
        self.tab.run_cdp("Network.setUserAgentOverride", **ua_param)
        return self
    
    def set_touch_mode(self, enabled=True, max_touch_points=1):
        # 如果 max_touch_points 为 0，强制禁用 touch 模式
        if max_touch_points == 0:
            enabled = False

        # 构造触摸模式参数，仅在 enabled 为 True 时包含 max_touch_points
        touch_mode_param = {
            "enabled": enabled
        }

        if enabled:  # 只有启用触摸模式时才添加 max_touch_points 参数
            touch_mode_param["max_touch_points"] = max_touch_points

        # 调用 CDP 方法
        self.tab.run_cdp("Emulation.setTouchEmulationEnabled", **touch_mode_param)
        return self
    
    def set_rpa_feature(self, enabled=True):
        set_rpa_feature_param={
            "enabled": enabled  # 启用或禁用自动化行为伪装 如果为 true，浏览器会伪装成正常的用户交互行为；如果为 false，则恢复自动化脚本的行为。
        }
        self.tab.run_cdp("Emulation.setAutomationOverride", **set_rpa_feature_param)
        return self

    def disable_cookies(self):
        disable_cookies_param={
            "disabled": True  # 禁用 document.cookie 访问
        }

        self.tab.run_cdp("Emulation.setDocumentCookieDisabled",**disable_cookies_param)
        return self

    def set_cpu_core(self,core=2):
        cpu_core_param={
            "hardwareConcurrency": core # 设置模拟的硬件并发数（CPU 核心数）
        }
        self.tab.run_cdp("Emulation.setHardwareConcurrencyOverride",**cpu_core_param)
        return self    

    def time_speed(self, policy='advance', budget=1000):

        if policy == "pause":
            param = {  
                "policy": "pause"
            }
        if policy == "advance":
            param = {
                "policy": "advance",
                "budget": budget
            }
        if policy == "realtime":
            param = {
                "policy": "realtime"
            }        
        self.tab.run_cdp("Emulation.setVirtualTimePolicy", **param)
        return self
    
    def set_locale(self, locale):  # 设置模拟的地理位置、语言和时区
        locale_param={
            "locale": locale,
        }
        self.tab.run_cdp("Emulation.setLocaleOverride", **locale_param)
        return self 
    
    def set_3d(self, x=1, y=0, z=0, alpha=10, beta=20, gamma=30):
        param = {
            "type":  "gyroscope" ,
            "reading": {
                "xyz": [x, y, z],
            }
        }
        self.tab.run_cdp("Emulation.setSensorOverrideReadings",**param)
        return self

    def set_size(self, width=360, height=740, mobile=True, scale=1):
        """
        mobile必须为true才能设置屏幕尺寸否则开启模拟后将被检测到使用固定屏幕尺寸，浏览器内窗口尺寸却会变化
        """
        size_param = {
                "width": width,              # 移动设备宽度
                "height": height,            # 移动设备高度
                "deviceScaleFactor": 1,      # DPI 比例
                "mobile": True,              # 设置为手机模式
                "scale": scale               # 页面缩放比例
        }
        self.tab.run_cdp("Emulation.setDeviceMetricsOverride", **size_param)

    def reset_size(self):
        self.tab.run_cdp('Emulation.clearDeviceMetricsOverride')
    