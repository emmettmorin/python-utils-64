import functools
import random
import time
from typing import Any, Callable, Dict


class RobloxAPIError(Exception):
    def __init__(self, message: str, status_code: int = 0, response_headers: Dict[str, str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.headers = response_headers or {}


class InvalidRobloxIDError(RobloxAPIError):
    pass


class RobloxRateLimitError(RobloxAPIError):
    pass


class RobloxTokenExpiredError(RobloxAPIError):
    pass


def validate_roblox_id(roblox_id: int, id_type: str = "User") -> int:
    """Validates 64-bit integer range for Roblox IDs."""
    if not isinstance(roblox_id, int) or roblox_id <= 0:
        raise InvalidRobloxIDError(f"Invalid Roblox {id_type} ID: '{roblox_id}'. Must be positive.", status_code=400)
    if roblox_id > 2**63 - 1:
        raise InvalidRobloxIDError(f"Roblox {id_type} ID {roblox_id} exceeds 64-bit integer limit.", status_code=400)
    return roblox_id


def handle_roblox_edge_cases(max_retries: int = 3, base_backoff: float = 0.5):
    """Decorator to intercept and recover from Roblox API edge cases and rate limits."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for key in ("user_id", "place_id", "universe_id", "asset_id", "group_id"):
                if key in kwargs and kwargs[key] is not None:
                    validate_roblox_id(kwargs[key], key.split("_")[0].capitalize())

            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except RobloxRateLimitError as err:
                    if retries >= max_retries:
                        raise err
                    retry_after = float(err.headers.get("Retry-After", base_backoff * (2 ** retries)))
                    jitter = random.uniform(0.05, 0.25)
                    time.sleep(retry_after + jitter)
                    retries += 1
                except RobloxTokenExpiredError as err:
                    csrf_token = err.headers.get("x-csrf-token")
                    if csrf_token and retries < 1:
                        kwargs["csrf_token"] = csrf_token
                        retries += 1
                        continue
                    raise err
                except KeyError as err:
                    raise RobloxAPIError(f"Malformed Roblox response payload, missing key: {err}", status_code=422) from err
        return wrapper
    return decorator
