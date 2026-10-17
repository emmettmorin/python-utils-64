import functools
import logging
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger("roblox-utils")

def robust_roblox_api(fallback: Any = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                logger.warning(f"Roblox endpoint unreachable: {e}")
                return fallback
            except KeyError as e:
                logger.error(f"Malformed Roblox API schema response: {e}")
                return fallback
            except Exception as e:
                logger.critical(f"Unanticipated Roblox runtime mutation: {e}")
                raise
        return wrapper
    return decorator

def sanitize_asset_id(value: Any) -> int:
    try:
        return int(str(value).split('/')[-1])
    except (ValueError, TypeError, IndexError):
        logger.debug(f"Invalid asset identifier supplied: {value}")
        return 0

class RobloxRateLimit(Exception):
    """Signal for backoff sequence execution."""
    pass

def check_status(response: Any) -> bool:
    if not response or not hasattr(response, "status_code"):
        return False
    if response.status_code == 429:
        raise RobloxRateLimit("Rate limited by Roblox servers")
    return response.status_code == 200