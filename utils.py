import time
import functools
import random

class NetworkRetryError(Exception):
    """Exception raised when network operations exceed retry limits."""
    pass

def retry_with_backoff(max_attempts=3, base_delay=1.0, jitter=True):
    """Decorator applying exponential backoff for Roblox API calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise NetworkRetryError(f"Failed after {max_attempts} attempts: {e}")
                    
                    delay = base_delay * (2 ** (attempts - 1))
                    if jitter:
                        delay += random.uniform(0, 0.1 * delay)
                    
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def execute_roblox_request(func, *args, **kwargs):
    """Higher-order function execution with baked-in retry logic."""
    retry_wrapper = retry_with_backoff()(func)
    return retry_wrapper(*args, **kwargs)