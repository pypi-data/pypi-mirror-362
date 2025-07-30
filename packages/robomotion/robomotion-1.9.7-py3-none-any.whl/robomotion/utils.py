from pathlib import Path
from sys import platform
from packaging import version
import os

class File:
    @staticmethod
    def temp_dir():
        home = str(Path.home())
        is_win = platform.startswith("win")
        if is_win:
            return "%s\\AppData\\Local\\Temp\\Robomotion" % home
        return "/tmp/robomotion"


class Version:
    @staticmethod
    def is_version_less_than(ver: str, other: str) -> bool:
        v = version.parse(ver)
        v2 = version.parse(other)
        return v < v2

def get_temp_path():
    if platform == "win32":
        home = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
        if home == "":
            home = os.getenv("USERPROFILE")
        return os.path.join(home, "AppData", "Local", "Robomotion", "temp")
    elif platform.startswith("linux") or platform == "darwin":
        return os.path.join(user_home_dir(), ".config", "robomotion", "temp")

    return ""

def user_home_dir():
    if platform == "win32":
        home = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
        if home == "":
            home = os.getenv("USERPROFILE")
        return home
    return os.getenv("HOME")