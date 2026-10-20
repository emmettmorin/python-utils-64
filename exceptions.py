class RobloxAPIError(Exception):
    """Base exception for all roblox-related operation failures."""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(f"[Roblox-64 Error {status_code}] {message}")
        self.status_code = status_code

class RateLimitExceeded(RobloxAPIError):
    """Raised when the 64-bit rate limiter triggers."""
    pass

class CookieInvalidated(RobloxAPIError):
    """Raised when .ROBLOSECURITY token is rejected by headers."""
    pass

class AssetResolutionFailure(RobloxAPIError):
    """Raised when asset IDs cannot be fetched from CDN."""
    pass

def graceful_reaper(func):
    """Decorator for trapping standard 64-bit edge cases."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            raise RobloxAPIError(f"Connectivity spike: {str(e)}", 503)
        except ValueError as e:
            raise AssetResolutionFailure(f"Malformed payload schema: {str(e)}", 400)
        except Exception as e:
            raise RobloxAPIError(f"Unclassified runtime collapse: {str(e)}", 500)
    return wrapper