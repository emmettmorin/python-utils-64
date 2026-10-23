"""Roblox API exception classes with dynamic context formatting."""

from typing import Any, Dict, Optional


class RobloxBaseException(Exception):
    """Base exception class for all python-utils-64 Roblox operations."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message: str = message
        self.status_code: Optional[int] = status_code
        self.details: Dict[str, Any] = details or {}
        super().__init__(self._format_payload())

    def _format_payload(self) -> str:
        code_tag = f" [HTTP {self.status_code}]" if self.status_code else ""
        context_info = f" | Meta: {self.details}" if self.details else ""
        return f"<{self.__class__.__name__}>{code_tag}: {self.message}{context_info}"


class CookieInvalidError(RobloxBaseException):
    """Raised when a provided .ROBLOSECURITY token is expired or malformed."""

    def __init__(self, token_hint: str = "???", **kwargs: Any) -> None:
        masked = token_hint[:4] + "..." + token_hint[-4:] if len(token_hint) >= 8 else "INVALID"
        super().__init__(
            f"Invalid security cookie supplied (Masked: {masked})",
            status_code=401,
            **kwargs,
        )


class RateLimitExceededError(RobloxBaseException):
    """Raised when hitting Roblox API rate limits (HTTP 429)."""

    def __init__(self, retry_after: float = 60.0, endpoint: str = "unknown", **kwargs: Any) -> None:
        self.retry_after: float = retry_after
        self.endpoint: str = endpoint
        details: Dict[str, Any] = kwargs.pop("details", {})
        details.update({"retry_after": retry_after, "endpoint": endpoint})
        super().__init__(
            f"Too many requests to endpoint '{endpoint}'",
            status_code=429,
            details=details,
            **kwargs,
        )


class AssetFetchError(RobloxBaseException):
    """Raised when failing to fetch asset meta or binary payload by asset ID."""

    def __init__(self, asset_id: int, reason: str = "Asset not found", **kwargs: Any) -> None:
        self.asset_id: int = asset_id
        details: Dict[str, Any] = kwargs.pop("details", {})
        details["asset_id"] = asset_id
        super().__init__(
            f"Failed to fetch asset #{asset_id}: {reason}",
            status_code=404,
            details=details,
            **kwargs,
        )
