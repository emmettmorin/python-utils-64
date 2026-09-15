import time
import functools
from typing import Callable, Any

def retry_request(retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class RobloxNetworkHandler:
    @retry_request(retries=5, delay=0.5)
    def fetch_asset(self, asset_id: int):
        # Simulated network call for Roblox API
        print(f"Fetching asset {asset_id}...")
        import random
        if random.random() < 0.7:
            raise ConnectionError("Roblox API throttled request")
        return {"id": asset_id, "status": "success"}