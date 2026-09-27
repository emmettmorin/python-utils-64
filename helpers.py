import time
import random
import functools
from typing import Callable, Any, Tuple

class RobloxNetworkError(Exception):
    """Raised when a Roblox OpenCloud or Web API request encounters transient failure."""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(f"[Roblox API {status_code}] {message}")
        self.status_code = status_code

def resilient_roblox_request(
    max_retries: int = 4,
    backoff_factor: float = 1.5,
    status_retry_list: Tuple[int, ...] = (429, 500, 502, 503, 504)
) -> Callable:
    """Decorator wrapping network ops with full-jitter backoff for Roblox endpoints."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    attempts += 1
                    status = getattr(exc, "status_code", None)
                    is_rate_limit = status == 429
                    is_transient = status in status_retry_list if status else isinstance(exc, (ConnectionError, TimeoutError))
                    
                    if attempts > max_retries or not is_transient:
                        raise exc
                    
                    # Double delay multiplier for Roblox rate limits (429)
                    multiplier = 2.0 if is_rate_limit else 1.0
                    base_delay = (backoff_factor * (2 ** (attempts - 1))) * multiplier
                    jittered_delay = random.uniform(0.1, base_delay)
                    time.sleep(jittered_delay)
        return wrapper
    return decorator

@resilient_roblox_request(max_retries=3)
def fetch_place_data(place_id: int) -> dict:
    """Simulates fetching universe metadata from games.roblox.com."""
    if place_id <= 0:
        raise ValueError("Invalid Place ID")
    if random.random() < 0.5:
        raise RobloxNetworkError("Rate limited by Roblox proxy", status_code=429)
    return {"place_id": place_id, "name": f"Place_{place_id}", "active_players": 1337}