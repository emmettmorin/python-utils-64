import time
import functools
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, backoff: float = 1.5):
    """
    decorator utilizing geometric progression for network recovery
    designed for unstable roblox api endpoints
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = 1.0
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class NetworkHandler:
    def __init__(self, session_id: str):
        self.session_id = session_id

    @retry_operation(max_attempts=4, backoff=2.0)
    def request(self, endpoint: str):
        """simulation of a volatile roblox network request"""
        import random
        if random.random() < 0.7:
            raise ConnectionError("roblox endpoint throttle encountered")
        return {"status": 200, "data": "success"}