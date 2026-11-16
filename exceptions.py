class RobloxAPIError(Exception):
    """Base exception for API interactions."""

class RateLimitExceeded(RobloxAPIError):
    """Raised when Roblox returns 429 status."""

class SessionInvalidated(RobloxAPIError):
    """Raised when the cookie or XCSRF token fails."""

class DataCorrupted(RobloxAPIError):
    """Raised when payload structure is unexpected."""

def handle_roblox_faults(func):
    """Decorator for graceful failure encapsulation."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            raise RobloxAPIError("Network connectivity lost while reaching endpoint")
        except (KeyError, TypeError) as e:
            raise DataCorrupted(f"Unexpected Roblox schema changes: {str(e)}")
        except Exception as e:
            if '429' in str(e):
                raise RateLimitExceeded("Backing off due to heavy request load")
            raise
    return wrapper

def validate_response(response):
    """Asserts success or throws typed exceptions."""
    status = getattr(response, 'status_code', 200)
    if status == 429:
        raise RateLimitExceeded("Throttled by Roblox cloud services")
    if status >= 500:
        raise RobloxAPIError("Internal server fault on Roblox backend")
    if status != 200:
        raise RobloxAPIError(f"Unhandled API fault code: {status}")