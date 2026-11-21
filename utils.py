import time
import functools
import random
from typing import Callable, Any

def exponential_backoff(retries: int = 3, base_delay: float = 1.0, jitter: bool = True):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == retries:
                        break
                    delay = base_delay * (2 ** attempt)
                    if jitter:
                        delay *= random.uniform(0.5, 1.5)
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def roblox_retry(max_attempts: int = 5):
    """Specialized wrapper for Roblox API rate limits."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_attempts - 1:
                        raise e
                    time.sleep(2 ** i + random.random())
        return wrapper
    return decorator