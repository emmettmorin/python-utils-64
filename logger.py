import datetime
import typing

class RobloxLogger:
    """Custom logger tailored for roblox data streams."""
    
    def __init__(self, prefix: str = "[RBX-64]") -> None:
        self.prefix: str = prefix

    def log(self, message: str, level: str = "INFO") -> None:
        """Formats and outputs logs with dynamic levels."""
        timestamp: str = datetime.datetime.now().strftime("%H:%M:%S")
        formatted: str = f"{self.prefix} {timestamp} [{level.upper()}]: {message}"
        print(formatted)

    def debug(self, data: typing.Any) -> None:
        """Specialized debug hook for complex Roblox tables."""
        self.log(f"DATA_DUMP: {str(data)}", "DEBUG")

    def warn(self, reason: str) -> None:
        """Warning stream for throttle and rate limits."""
        self.log(reason, "WARN")

def create_logger(name: str = "default") -> RobloxLogger:
    """Factory function returning a configured instance."""
    return RobloxLogger(prefix=f"[{name.upper()}-64]")