import random
import time
import urllib.error
import urllib.request
from typing import Callable, Any, Optional, TypeVar, Tuple

T = TypeVar('T')

class RobloxNetworkError(Exception):
    """Raised when a Roblox network operation exhausts all retries."""
    pass

def _fibonacci_jitter_sequence(base_delay: float, max_delay: float):
    a, b = 1, 1
    while True:
        delay = min(base_delay * a + random.uniform(0.05, 0.3), max_delay)
        yield delay
        a, b = b, a + b

def roblox_retry(
    max_attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 10.0,
    retryable_status_codes: Tuple[int, ...] = (429, 500, 502, 503, 504)
) -> Callable:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delays = _fibonacci_jitter_sequence(base_delay, max_delay)
            last_exception: Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except urllib.error.HTTPError as err:
                    last_exception = err
                    if err.code not in retryable_status_codes or attempt == max_attempts:
                        raise RobloxNetworkError(f"HTTP {err.code} failure after {attempt} attempt(s)") from err
                except urllib.error.URLError as err:
                    last_exception = err
                    if attempt == max_attempts:
                        raise RobloxNetworkError(f"URL error after {attempt} attempt(s)") from err

                sleep_time = next(delays)
                time.sleep(sleep_time)

            raise RobloxNetworkError(f"Retry limit reached ({max_attempts})") from last_exception
        return wrapper
    return decorator

@roblox_retry(max_attempts=3, base_delay=0.2)
def fetch_roblox_user_info(user_id: int) -> str:
    url = f"https://users.roblox.com/v1/users/{user_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "PythonRobloxUtil/1.0"})
    with urllib.request.urlopen(req, timeout=5.0) as response:
        return response.read().decode('utf-8')
