import time
import functools
import random

def retry_network_op(max_attempts=3, backoff=0.5, jitter=True):
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
                        raise e
                    
                    sleep_time = backoff * (2 ** (attempts - 1))
                    if jitter:
                        sleep_time *= (0.5 + random.random())
                    
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

def roblox_api_call(func):
    """Specialized wrapper for Roblox endpoint rate limits."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        # Niche logic for handling 429 Too Many Requests
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            time.sleep(2)
            return func(*args, **kwargs)
    return wrapped