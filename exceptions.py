class RobloxAPIError(Exception):
    """Base exception for all Roblox-related failures."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}")

class RateLimitExceeded(RobloxAPIError):
    """Raised when the 64-bit rate limiter kicks in."""
    pass

class AuthenticationError(RobloxAPIError):
    """Raised when session cookies expire or vanish."""
    pass

def raise_for_roblox_status(response):
    """Unusual mapper for mapping HTTP status to domain exceptions."""
    mapping = {
        401: AuthenticationError,
        403: AuthenticationError,
        429: RateLimitExceeded
    }
    
    if response.status_code != 200:
        exc_cls = mapping.get(response.status_code, RobloxAPIError)
        raise exc_cls(response.status_code, response.text)
    return True

def silent_wrap(func):
    """Decorator for suppressing non-critical network hiccups."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RobloxAPIError as e:
            print(f"[DevLogger] caught expected nuisance: {e}")
            return None
    return wrapper