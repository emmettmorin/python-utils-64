import time
import urllib.request
import urllib.error
import json
import random
from functools import wraps
from typing import Callable, Any, Dict

class RobloxNetworkError(Exception):
    """Raised when a Roblox API request exhausts all retry attempts."""
    pass

def roblox_retry(
    max_attempts: int = 5,
    base_backoff: float = 1.0,
    backoff_factor: float = 2.0,
    status_codes: tuple = (429, 500, 502, 503, 504)
) -> Callable:
    """
    Decorator that retries Roblox API requests with dynamic jitter 
    and automatic 'Retry-After' header extraction.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                attempts += 1
                try:
                    return func(*args, **kwargs)
                except urllib.error.HTTPError as err:
                    if err.code not in status_codes or attempts == max_attempts:
                        raise RobloxNetworkError(f"Roblox API failed [HTTP {err.code}]: {err.reason}") from err
                    
                    retry_after = err.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_time = float(retry_after)
                    else:
                        jitter = random.uniform(0.1, 0.5)
                        wait_time = (base_backoff * (backoff_factor ** (attempts - 1))) + jitter
                    
                    time.sleep(wait_time)
                except urllib.error.URLError as err:
                    if attempts == max_attempts:
                        raise RobloxNetworkError(f"Roblox connection unreachable: {err.reason}") from err
                    time.sleep(base_backoff * attempts)
        return wrapper
    return decorator

@roblox_retry(max_attempts=3)
def fetch_roblox_user(user_id: int) -> Dict[str, Any]:
    """Fetch basic user details from Roblox API with automated retries."""
    url = f"https://users.roblox.com/v1/users/{user_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "python-utils-64/1.0"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))
