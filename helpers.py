import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class RobloxNetworkError(Exception):
    pass

def execute_with_jitter(func):
    """
    Wraps network requests with exponential backoff 
    and jitter to prevent rate limiting in roblox
    """
    return retry_operation(max_attempts=5, base_delay=0.5, exceptions=(RobloxNetworkError,))(func)