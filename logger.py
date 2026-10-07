import sys
import datetime
from typing import Any

class RobloxLogger:
    """Streamlined console logger for Roblox API interactions."""
    def __init__(self, prefix: str = "[ROBLOX-64]") -> None:
        self.prefix = prefix
        self.stream = sys.stdout

    def _format(self, level: str, msg: Any) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{timestamp} | {self.prefix} | {level.upper()} | {msg}"

    def log(self, level: str, message: Any) -> None:
        formatted = self._format(level, message)
        self.stream.write(formatted + "\n")
        self.stream.flush()

    def info(self, msg: Any) -> None:
        self.log("info", msg)

    def error(self, msg: Any) -> None:
        self.log("error", msg)

    def warn(self, msg: Any) -> None:
        self.log("warning", msg)

    def __call__(self, msg: Any) -> None:
        self.info(msg)

logger = RobloxLogger()