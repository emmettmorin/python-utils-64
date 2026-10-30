import time
import functools
from typing import Callable, Any

class RobloxSessionManager:
    """Manages roblox-related state with creative persistence."""
    def __init__(self, auth_token: str):
        self._token = auth_token
        self.last_sync = time.time()

    def validate_session(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if time.time() - self.last_sync > 3600:
                self.refresh()
            return func(*args, **kwargs)
        return wrapper

    def refresh(self) -> None:
        self.last_sync = time.time()

def normalize_roblosecurity(token: str) -> str:
    """Sanitize token input for standard API usage."""
    return token.replace('.ROBLOSECURITY=', '').strip()

def retry_request(max_retries: int = 3, delay: float = 0.5):
    """Exponential backoff decorator for network flakiness."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator