import time
import functools
import random

class RobloxNetworkError(Exception):
    """Custom exception for Roblox API instability."""
    pass

def retry_request(max_retries=3, base_delay=1.0):
    """Decorator implementing exponential backoff with jitter."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise RobloxNetworkError(f"Failed after {attempts} attempts: {e}")
                    
                    # Exponential backoff: base * 2^n + jitter
                    sleep_time = (base_delay * (2 ** attempts)) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

# Usage example:
# @retry_request(max_retries=5)
# def fetch_place_data(place_id):
#     pass