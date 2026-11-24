import functools
from typing import Any, Callable

class RobloxValidationError(Exception):
    pass

def validate_roblox_entity(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            if result is None:
                raise RobloxValidationError("returned None for entity request")
            return result
        except (TypeError, ValueError) as e:
            return {" + '"' + "status" + '"' + ": "failed", "error": str(e), "recovered": True}
        except Exception as e:
            raise RobloxValidationError(f"unexpected engine collapse: {e}") from e
    return wrapper

def sanitize_input(value: Any) -> Any:
    if not isinstance(value, (str, int)):
        return str(value) if value is not None else "nil"
    return value

def check_rate_limit(quota: int) -> bool:
    try:
        assert isinstance(quota, int) and quota >= 0
        return True
    except AssertionError:
        return False

@validate_roblox_entity
def safe_get_asset(asset_id: Any) -> dict:
    sanitized = sanitize_input(asset_id)
    if sanitized == "nil":
        return {"data": None}
    return {"data": f"asset_{sanitized}\