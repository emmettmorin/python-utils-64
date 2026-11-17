import sys
import datetime
from typing import Any

class RobloxLogger:
    COLORS = {"INFO": "\033[94m", "WARN": "\033[93m", "ERROR": "\033[91m", "RESET": "\033[0m"}

    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode

    def _log(self, level: str, message: Any) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = self.COLORS.get(level, self.COLORS["RESET"])
        print(f"{color}[{level}] [{timestamp}] {message}{self.COLORS['RESET']}")

    def info(self, msg: Any) -> None:
        self._log("INFO", msg)

    def warn(self, msg: Any) -> None:
        self._log("WARN", msg)

    def error(self, msg: Any) -> None:
        self._log("ERROR", msg)

    def debug(self, msg: Any) -> None:
        if self.debug_mode:
            self._log("DEBUG", msg)

def get_logger(name: str = "roblox-utils") -> RobloxLogger:
    return RobloxLogger()