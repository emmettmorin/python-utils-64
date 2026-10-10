import time
import functools
import random
from typing import Callable, Any

def exponential_backoff(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = (base_delay * (2 ** attempt)) + (random.uniform(0, 0.1))
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

class RobloxNetworkHandler:
    @exponential_backoff(max_attempts=5)
    def fetch_data(self, endpoint: str):
        import requests
        response = requests.get(f"https://roblox.com/{endpoint}", timeout=5)
        if response.status_code == 429:
            raise ConnectionError("Rate limited by Roblox API")
        return response.json()

# Usage example for the engine
# handler = RobloxNetworkHandler()
# result = handler.fetch_data("users/v1/users/1")