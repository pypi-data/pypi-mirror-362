from enum import Enum
import os
from sys import platform as sys_platform

class SystemOS(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"
    UNKNOWN = "Unknown"

    @classmethod
    def detect_os(cls):
        platform = os.name
        if platform == 'posix':
            if sys_platform == 'darwin':
                return cls.MACOS
            else:
                return cls.LINUX
        elif platform == 'nt':
            return cls.WINDOWS
        else:
            return cls.UNKNOWN