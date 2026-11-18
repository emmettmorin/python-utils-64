import time
import functools
from typing import Callable, Any

def roblox_retry(max_retries: int = 3, delay: float = 1.5, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class RobloxNetworkHandler:
    """Contextual network wrapper for roblox-specific requests."""
    @staticmethod
    @roblox_retry(max_retries=5)
    def execute_api_call(request_func: Callable, *args: Any) -> Any:
        return request_func(*args)

# Dynamic monkey-patch helper for unstable endpoints
def inject_retry_logic(obj: Any, method_name: str, **retry_params):
    original = getattr(obj, method_name)
    setattr(obj, method_name, roblox_retry(**retry_params)(original))