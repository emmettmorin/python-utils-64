import time
import functools
import random
from typing import Callable, Any

def retry_network_op(max_attempts: int = 3, base_delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    wait = base_delay * (2 ** attempt) + (random.uniform(0, 0.1))
                    time.sleep(wait)
            raise last_ex
        return wrapper
    return decorator

class RobloxNetworkHandler:
    def __init__(self, session_id: str):
        self.session_id = session_id

    @retry_network_op(max_attempts=4)
    def fetch_universe_data(self, universe_id: int):
        # Simulated unstable roblox api call
        if random.random() < 0.7:
            raise ConnectionError('Roblox API throttled')
        return {'id': universe_id, 'status': 'online', 'ts': time.time()}