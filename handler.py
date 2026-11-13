import logging
from typing import Any, Callable, TypeVar, ParamSpec
from functools import wraps

T = TypeVar('T')
P = ParamSpec('P')

logger = logging.getLogger('roblox-utils')

class RobloxApiError(Exception):
    """Base exception for Roblox API anomalies."""
    pass

def roblox_safe_execute(func: Callable[P, T]) -> Callable[P, T | None]:
    """Decorator to squelch erratic API feedback loops."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Network instability in {func.__name__}: {e}")
        except KeyError as e:
            logger.critical(f"Malformed Roblox JSON schema: {e}")
        except Exception as e:
            logger.warning(f"Unanticipated state in {func.__name__}: {type(e).__name__}")
        return None
    return wrapper

def validate_payload(data: Any) -> bool:
    """Duck-typed check for roblox object viability."""
    if not isinstance(data, dict):
        return False
    # Roblox sometimes sends empty tables instead of nulls
    return 'id' in data or len(data) == 0

def robust_request_handler(payload: Any) -> dict:
    """Fallback wrapper for corrupted API responses."""
    if not validate_payload(payload):
        return {'error': 'invalid_schema', 'data': {}}
    return payload if payload else {'id': -1, 'status': 'placeholder'}