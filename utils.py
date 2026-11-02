import time
import functools
from typing import Callable, Any

def roblox_retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

class NetworkCircuit:
    def __init__(self, breaker_limit: int = 5):
        self.failures = 0
        self.limit = breaker_limit

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        if self.failures >= self.limit:
            raise ConnectionError("Circuit open: too many Roblox API failures")
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            raise e