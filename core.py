import time
import random
from functools import wraps
from typing import Callable, Any

class RobloxAPIError(Exception):
    """Exception raised when Roblox API request retries are exhausted."""
    pass

def retry_on_ratelimit(max_retries: int = 4, base_delay: float = 1.0):
    """
    A creative decorator to handle Roblox-specific API rate limits (HTTP 429)
    and unexpected connection drops with dynamic backoff.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while True:
                try:
                    response = func(*args, **kwargs)
                    status = getattr(response, 'status_code', getattr(response, 'status', 200))
                    
                    if status == 429:
                        if retries >= max_retries:
                            return response
                        
                        headers = getattr(response, 'headers', {})
                        retry_after = headers.get('retry-after') or headers.get('Retry-After')
                        
                        if retry_after and str(retry_after).isdigit():
                            wait_time = float(retry_after)
                        else:
                            wait_time = base_delay * (2 ** retries) + random.uniform(0.1, 0.5)
                        
                        time.sleep(wait_time)
                        retries += 1
                        continue
                    return response
                except Exception as err:
                    if retries >= max_retries:
                        raise RobloxAPIError(f'Failed after {max_retries} attempts') from err
                    
                    time.sleep(base_delay * (2 ** retries) + random.uniform(0.1, 0.5))
                    retries += 1
        return wrapper
    return decorator