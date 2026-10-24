import sys
from typing import Any, Dict, Optional


class RobloxExceptionMeta(type):
    """Metaclass for dynamically mapping Roblox internal error codes to exceptions."""

    _registry: Dict[int, type] = {}

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        new_cls = super().__new__(cls, name, bases, attrs)
        code = attrs.get("error_code")
        if code is not None and isinstance(code, int):
            cls._registry[code] = new_cls
        return new_cls

    @classmethod
    def resolve_code(cls, code: int) -> type:
        return cls._registry.get(code, RobloxAPIError)


class RobloxAPIError(Exception, metaclass=RobloxExceptionMeta):
    """Base exception class for all Roblox API operations."""

    error_code: Optional[int] = None
    default_message: str = "An unknown Roblox API error occurred."

    def __init__(
        self, message: Optional[str] = None, *, status_code: int = 400, details: Optional[Dict[str, Any]] = None
    ):
        self.message = message or self.default_message
        self.status_code = status_code
        self.details = details or {}
        tag = f"{self.status_code}:{self.error_code or 'GENERIC'}"
        super().__init__(f"[{tag}] {self.message}")

    def as_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "code": self.error_code,
            "status": self.status_code,
            "message": self.message,
            "details": self.details,
        }


class CookieInvalidError(RobloxAPIError):
    error_code = 4010
    default_message = "The provided .ROBLOSECURITY cookie is invalid or expired."


class AssetPermissionError(RobloxAPIError):
    error_code = 4030
    default_message = "Insufficient permissions to access or modify this asset."


class DatastoreRateLimitError(RobloxAPIError):
    error_code = 4290
    default_message = "Roblox DataStore key or request budget exceeded."


class PlaceNotFoundError(RobloxAPIError):
    error_code = 4040
    default_message = "Target universe or place ID could not be found."


def raise_for_roblox_code(code: int, custom_msg: Optional[str] = None, **kwargs) -> None:
    """Factory helper throwing mapped exception based on internal Roblox status code."""
    exc_cls = RobloxExceptionMeta.resolve_code(code)
    raise exc_cls(message=custom_msg, details=kwargs)
