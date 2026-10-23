import time
import functools
from typing import Callable, Any

def rate_limit(calls: int, period: float) -> Callable:
    """Decorator for Roblox API request throttling."""
    def decorator(func: Callable) -> Callable:
        history = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            now = time.time()
            nonlocal history
            history = [t for t in history if now - t < period]
            if len(history) >= calls:
                time.sleep(period - (now - history[0]))
            result = func(*args, **kwargs)
            history.append(time.time())
            return result
        return wrapper
    return decorator

def clean_robux_string(value: str) -> int:
    """Sanitization for currency strings returned by API."""
    if not isinstance(value, str):
        return 0
    return int(''.join(filter(str.isdigit, value)) or 0)

class RobloxSessionManager:
    """Context-based handler for studio API interactions."""
    def __init__(self, auth_token: str):
        self.token = auth_token
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.token = None

def format_asset_id(asset_id: Any) -> str:
    """Ensures consistent asset identifier formatting."""
    return f"rbxassetid://{str(asset_id).strip()}"