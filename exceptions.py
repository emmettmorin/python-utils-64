import sys
from typing import Any, Dict, Optional


class RobloxExceptionMeta(type):
    """Metaclass to auto-register edge-case error codes to exception types."""

    _registry: Dict[int, type] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        error_code = attrs.get("ERROR_CODE")
        if error_code is not None:
            mcs._registry[error_code] = cls
        return cls

    @classmethod
    def dispatch(cls, error_code: int, message: str, **details) -> "RobloxAPIError":
        target_cls = cls._registry.get(error_code, RobloxAPIError)
        return target_cls(message, error_code=error_code, **details)


class RobloxAPIError(Exception, metaclass=RobloxExceptionMeta):
    """Base exception for Roblox API interactions with contextual payloads."""

    ERROR_CODE: Optional[int] = None

    def __init__(self, message: str, error_code: Optional[int] = None, **details: Any):
        self.message = message
        self.error_code = error_code or self.ERROR_CODE or -1
        self.details = details
        super().__init__(f"[{self.error_code}] {self.message}")

    def sanitize_context(self) -> Dict[str, Any]:
        """Mask sensitive tokens or ROBLOSECURITY cookies in details."""
        sanitized = {}
        for k, v in self.details.items():
            if "cookie" in k.lower() or "token" in k.lower():
                sanitized[k] = "[REDACTED_SECURITY_TOKEN]"
            else:
                sanitized[k] = v
        return sanitized


class RateLimitExceeded(RobloxAPIError):
    ERROR_CODE = 429

    def __init__(self, message: str = "Too many requests", retry_after: float = 60.0, **details: Any):
        super().__init__(message, error_code=429, retry_after=retry_after, **details)
        self.retry_after = retry_after


class AssetModeratedError(RobloxAPIError):
    ERROR_CODE = 4031

    def __init__(self, message: str = "Asset blocked by moderation", asset_id: int = 0, **details: Any):
        super().__init__(message, error_code=4031, asset_id=asset_id, **details)
        self.asset_id = asset_id


class UniverseNotFound(RobloxAPIError):
    ERROR_CODE = 4040

    def __init__(self, message: str = "Target place or universe missing", universe_id: int = 0, **details: Any):
        super().__init__(message, error_code=4040, universe_id=universe_id, **details)
        self.universe_id = universe_id


def raise_for_roblox_error(status_code: int, body: Dict[str, Any], token: Optional[str] = None):
    """Dynamic edge-case dispatcher converting API payloads into rich errors."""
    errors = body.get("errors", [])
    msg = errors[0].get("message", "Unknown Roblox API fault") if errors else "API fault"
    code = errors[0].get("code", status_code) if errors else status_code
    raise RobloxExceptionMeta.dispatch(code, msg, raw_body=body, auth_token=token)
