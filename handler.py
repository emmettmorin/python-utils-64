import functools
import math
import re
from typing import Any, Callable, Dict, Optional, Type, Union


class RobloxAPIError(Exception):
    """Base exception for Roblox API communications."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AssetIdInvalidError(RobloxAPIError):
    """Raised when a given Roblox Asset ID or URL is malformed."""


class RateLimitExceeded(RobloxAPIError):
    """Raised when Roblox Open Cloud or Web API hits 429."""


def safe_asset_extractor(fallback_id: int = 0) -> Callable:
    """Decorator that handles chaotic user input for Roblox Asset IDs.

    Extracts numeric IDs from URLs, deep links, or raw strings while catching
    out-of-bounds integers and malformed protocols safely.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(val: Union[str, int, float], *args: Any, **kwargs: Any) -> Any:
            try:
                if isinstance(val, float):
                    if math.isnan(val) or math.isinf(val) or val <= 0:
                        raise AssetIdInvalidError(f"Invalid floating-point asset ID: {val}")
                    val = int(val)

                if isinstance(val, str):
                    match = re.search(r'(?:rbxassetid://|/catalog/|/library/)?(\d{5,12})', val)
                    if not match:
                        raise AssetIdInvalidError(f"Could not parse valid Roblox asset ID from: {val!r}")
                    val = int(match.group(1))

                if isinstance(val, int):
                    if not (1 <= val <= 9_999_999_999_999):
                        raise AssetIdInvalidError(f"Asset ID out of bounds for Roblox system: {val}")

                return func(val, *args, **kwargs)

            except AssetIdInvalidError as err:
                if fallback_id > 0:
                    return func(fallback_id, *args, **kwargs)
                raise err
            except (TypeError, ValueError) as err:
                raise RobloxAPIError(f"Unexpected input type parsing asset ID: {type(val).__name__}") from err

        return wrapper
    return decorator


class EdgeCaseResponseHandler:
    """Processes Roblox HTTP responses with dynamic exception mapping."""

    @staticmethod
    def handle_response(status: int, body: Dict[str, Any]) -> Dict[str, Any]:
        if status == 200:
            return body or {"status": "success"}

        error_map: Dict[int, Type[RobloxAPIError]] = {
            429: RateLimitExceeded,
            401: RobloxAPIError,
            403: RobloxAPIError,
            404: AssetIdInvalidError,
        }

        err_cls = error_map.get(status, RobloxAPIError)
        messages = body.get("errors", [{}]) if isinstance(body, dict) else []
        msg = messages[0].get("message") if messages else f"Roblox API returned status {status}"

        raise err_cls(f"Roblox HTTP {status}: {msg}", status_code=status)
