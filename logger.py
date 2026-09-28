import logging
from typing import Any, Optional

class RobloxLogger:
    """Custom logger for roblox-based automation scripts."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self._logger: logging.Logger = logging.getLogger(name)
        self._logger.setLevel(level)
        handler: logging.StreamHandler = logging.StreamHandler()
        fmt: str = "[%(asctime)s] [%(levelname)s] - %(message)s"
        handler.setFormatter(logging.Formatter(fmt))
        self._logger.addHandler(handler)

    def info(self, message: Any) -> None:
        """Log an informational event with style."""
        self._logger.info(str(message))

    def debug_payload(self, data: Any) -> None:
        """Hex-dump style logging for network payloads."""
        self._logger.debug(f"RAW_DATA: {repr(data)}")

    def error_critical(self, exception: Exception, context: Optional[str] = None) -> None:
        """Format exceptions for easier Roblox API debugging."""
        ctx_str: str = f" ({context})" if context else ""
        self._logger.error(f"CRITICAL_FAILURE{ctx_str}: {type(exception).__name__} -> {str(exception)}")