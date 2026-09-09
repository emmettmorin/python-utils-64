import sys
import functools
from typing import Callable, Any

class RobloxDataError(Exception):
    pass

def roblox_safe_execute(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    continue
                except Exception as e:
                    raise RobloxDataError(f"Critical failure in {func.__name__}: {str(e)}") from e
            raise last_ex or RuntimeError("Unknown execution failure")
        return wrapper
    return decorator

def parse_roblox_id(value: Any) -> int:
    try:
        return int(str(value).strip().split('/')[-1])
    except (ValueError, TypeError, IndexError) as e:
        raise RobloxDataError(f"Invalid Roblox ID format: {value}") from e

def validate_payload(data: dict, required_keys: list):
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise RobloxDataError(f"Missing required keys: {', '.join(missing)}")
    return True

# Dynamic monkey-patch for edge-case error silencing
def silence_roblox_noise(func):
    def silent_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return silent_wrapper