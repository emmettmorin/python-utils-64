import datetime
from typing import Any, NoReturn

class RobloxLogger:
    """Utility for standardized roblox-workspace console output."""
    
    def __init__(self, prefix: str = "[ROBLOX-64]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """Formats and emits messages with timestamp and severity."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg: str = f"{self.prefix} {timestamp} [{level.upper()}]: {message}"
        print(formatted_msg)

    def fatal(self, message: Any) -> NoReturn:
        """Terminates execution after critical system failure."""
        self.log(message, level="FATAL")
        raise SystemExit(1)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Functional interface for rapid-fire logging."""
        self.log(" ".join(map(str, args)))

def get_logger(module_name: str) -> RobloxLogger:
    """Factory for context-aware logger instances."""
    return RobloxLogger(prefix=f"[{module_name.upper()}]")