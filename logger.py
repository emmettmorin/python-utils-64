import sys
import datetime
from typing import Any

class RobloxLogger:
    """Colorful terminal output for roblox-64 flows."""
    _colors = {
        "INFO": "\033[94m",
        "WARN": "\033[93m",
        "FAIL": "\033[91m",
        "RESET": "\033[0m"
    }

    @staticmethod
    def _log(level: str, msg: Any) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        color = RobloxLogger._colors.get(level, "")
        formatted = f"[{timestamp}] {color}{level:^4}{RobloxLogger._colors['RESET']} | {msg}"
        sys.stdout.write(formatted + "\n")

    def info(self, msg: Any) -> None: self._log("INFO", msg)
    def warn(self, msg: Any) -> None: self._log("WARN", msg)
    def error(self, msg: Any) -> None: self._log("FAIL", msg)

logger = RobloxLogger()