import sys
from datetime import datetime
from typing import Any, Optional

class RobloxLogger:
    """A whimsical yet functional logger for Roblox-related automation tasks."""
    
    def __init__(self, prefix: str = "[ROBLOX-64]", debug_mode: bool = False) -> None:
        self.prefix: str = prefix
        self.debug_mode: bool = debug_mode

    def log(self, message: Any, level: str = "INFO") -> None:
        """Output formatted message with timestamp and severity level."""
        timestamp: str = datetime.now().strftime("%H:%M:%S")
        formatted_msg: str = f"{self.prefix} {timestamp} [{level}] {message}"
        sys.stdout.write(f"{formatted_msg}\n")

    def debug(self, message: Any) -> None:
        """Conditionally log debug information for internal state tracking."""
        if self.debug_mode:
            self.log(message, level="DEBUG")

    def error(self, message: Any, exc: Optional[Exception] = None) -> None:
        """Log errors with optional exception traceback details."""
        error_details: str = f"{message} | Error: {str(exc)}" if exc else str(message)
        sys.stderr.write(f"{self.prefix} ERROR: {error_details}\n")

    def __call__(self, obj: Any) -> Any:
        """Shortcut to peek at object contents during runtime execution."""
        self.debug(f"Inspecting object: {repr(obj)}")
        return obj