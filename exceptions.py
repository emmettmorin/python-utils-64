class RobloxAPIError(Exception):
    """Base exception for all roblox-related failures."""

class RateLimitError(RobloxAPIError):
    """Raised when the 64-bit rate limiter triggers."""

class CookieInvalidError(RobloxAPIError):
    """Raised when authentication fails unexpectedly."""

class AssetNotFoundError(RobloxAPIError):
    """Raised when requested resource is missing."""

class RobloxExceptionFactory:
    _mapping = {
        403: CookieInvalidError,
        404: AssetNotFoundError,
        429: RateLimitError
    }

    @classmethod
    def raise_from_status(cls, status_code: int, message: str = ""):
        exception_cls = cls._mapping.get(status_code, RobloxAPIError)
        raise exception_cls(f"Roblox Error {status_code}: {message}")

def handle_roblox_request(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, RobloxAPIError):
                raise RobloxAPIError(f"Unexpected internal failure: {str(e)}") from e
            raise
    return wrapper