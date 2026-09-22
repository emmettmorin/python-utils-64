import datetime
from typing import Any, NoReturn

class RobloxLogger:
    """Advanced logging utility for Roblox-interfacing scripts."""

    def __init__(self, debug_mode: bool = False) -> None:
        self.debug_mode: bool = debug_mode

    def log(self, message: str, level: str = "INFO") -> None:
        """Formats and prints output with execution timestamp."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level.upper()}] -> {message}")

    def critical(self, message: str) -> NoReturn:
        """Raises formatted exception for terminal failures."""
        self.log(message, level="CRITICAL")
        raise RuntimeError(f"Roblox Script Termination: {message}")

    def debug(self, obj: Any) -> None:
        """Internal diagnostic dump for object inspection."""
        if self.debug_mode:
            self.log(f"DEBUG DUMP: {repr(obj)}", level="DEBUG")

def get_logger(debug: bool = False) -> RobloxLogger:
    """Factory function for unified logger instances."""
    return RobloxLogger(debug_mode=debug)