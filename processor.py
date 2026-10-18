import time
import functools
import random
from typing import Callable, Any

def retry_roblox_api(retries: int = 3, backoff: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = backoff * (2 ** attempt) + (random.randint(0, 1000) / 1000)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class RobloxNetworkProcessor:
    def __init__(self, session_id: str):
        self.session_id = session_id

    @retry_roblox_api(retries=5, backoff=0.5)
    def fetch_universe_data(self, universe_id: int):
        # Simulated unstable network request logic
        if random.random() < 0.7:
            raise ConnectionError("Roblox API throttling detected")
        return {"id": universe_id, "status": "online", "sid": self.session_id}