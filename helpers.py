import random
import time
import urllib.error
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


class RobloxRequestEngine:
    def __init__(self, max_retries: int = 4, base_delay: float = 1.0, max_delay: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def _calculate_jitter_delay(self, attempt: int, response_headers: Optional[dict] = None) -> float:
        if response_headers and "retry-after" in response_headers:
            try:
                return float(response_headers["retry-after"])
            except (ValueError, TypeError):
                pass
        
        exponential = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0.5, 1.5)
        return min(self.max_delay, exponential * jitter)

    def execute_with_retry(self, request_fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                return request_fn(*args, **kwargs)
            except urllib.error.HTTPError as err:
                last_exception = err
                if err.code not in (429, 500, 502, 503, 504) or attempt == self.max_retries:
                    raise
                headers = {k.lower(): v for k, v in err.headers.items()} if err.headers else {}
                delay = self._calculate_jitter_delay(attempt, headers)
                time.sleep(delay)
            except (urllib.error.URLError, ConnectionError) as err:
                last_exception = err
                if attempt == self.max_retries:
                    raise
                delay = self._calculate_jitter_delay(attempt)
                time.sleep(delay)
        
        if last_exception:
            raise last_exception


def roblox_retry(max_retries: int = 3, base_delay: float = 0.5):
    engine = RobloxRequestEngine(max_retries=max_retries, base_delay=base_delay)
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return engine.execute_with_retry(func, *args, **kwargs)
        return wrapper
    return decorator
