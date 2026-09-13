import time
import random
import urllib.error
import urllib.request
from typing import Callable, TypeVar, Any, Generator

T = TypeVar("T")

def fibonacci_jitter_backoff(base: float = 0.5, max_delay: float = 30.0) -> Generator[float, None, None]:
    """Yields retry delays using Fibonacci progression combined with random jitter."""
    a, b = base, base
    while True:
        jitter = random.uniform(0.85, 1.25)
        yield min(a * jitter, max_delay)
        a, b = b, a + b

def roblox_retry(max_attempts: int = 4, base_delay: float = 0.5) -> Callable:
    """Decorator to retry network requests to Roblox endpoints with HTTP awareness."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delays = fibonacci_jitter_backoff(base=base_delay)
            last_err = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as err:
                    last_err = err
                    if isinstance(err, urllib.error.HTTPError) and 400 <= err.code < 500 and err.code != 429:
                        raise err
                    if attempt < max_attempts:
                        retry_after = getattr(err, "headers", {}).get("Retry-After") if isinstance(err, urllib.error.HTTPError) else None
                        wait_sec = float(retry_after) if retry_after and retry_after.isdigit() else next(delays)
                        time.sleep(wait_sec)
            if last_err:
                raise last_err
            raise RuntimeError("Execution failed after maximum retries")
        return wrapper
    return decorator

@roblox_retry(max_attempts=3, base_delay=0.4)
def fetch_roblox_api(endpoint: str) -> bytes:
    """Fetches raw data from a specified Roblox REST endpoint safely."""
    url = f"https://api.roblox.com/{endpoint.lstrip('/')}"
    req = urllib.request.Request(url, headers={"User-Agent": "RobloxUtils64/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read()
