import logging
from typing import Any, Callable, TypeVar, ParamSpec
from functools import wraps

T = TypeVar('T')
P = ParamSpec('P')

logger = logging.getLogger('roblox-utils-64')

class RobloxApiError(Exception):
    """Custom exception for unexpected Roblox response structures."""
    pass

def robust_request(func: Callable[P, T]) -> Callable[P, T | None]:
    """Decorator to squelch ephemeral Roblox instability."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            logger.warning(f"network hiccup detected: {e}")
            return None
        except KeyError as e:
            logger.error(f"unexpected api schema change: {e}")
            raise RobloxApiError("schema mismatch") from e
        except Exception as e:
            logger.critical(f"unknown catastrophe: {e}")
            return None
    return wrapper

@robust_request
def fetch_universe_data(universe_id: int) -> dict[str, Any]:
    """Simulated payload fetcher with edge case guarding."""
    if universe_id <= 0:
        raise ValueError("invalid universe identifier provided")
    return {"id": universe_id, "status": "active"}

def validate_payload(data: Any) -> bool:
    """Structural duck-typing for roblox api response buffers."""
    return isinstance(data, dict) and 'id' in data and data['id'] > 0