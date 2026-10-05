import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.5))
                    current_delay *= backoff
        return wrapper
    return decorator

def roblox_api_retry(func: Callable):
    @functools.wraps(func)
    @retry_operation(max_attempts=5, delay=0.5, backoff=1.5)
    def managed_request(*args, **kwargs):
        return func(*args, **kwargs)
    return managed_request