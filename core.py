import re
import time
from typing import Any, Callable, Dict, Union

class RobloxAPIError(Exception):
    """Custom exception raised for unparseable or faulty Roblox API responses."""
    pass

class RobloxEdgeCaseHandler:
    """Resilient decorator handling string IDs, HTML responses, and unexpected rate limits."""

    @staticmethod
    def sanitize_id(identifier: Union[int, str, float]) -> int:
        if isinstance(identifier, float):
            identifier = int(identifier)
        cleaned = re.sub(r"[^\d-]", "", str(identifier))
        if not cleaned:
            raise ValueError(f"Invalid Roblox ID format: {identifier}")
        val = int(cleaned)
        if val <= 0:
            raise ValueError(f"Roblox IDs must be positive integers, got: {val}")
        return val

    @classmethod
    def safe_api_call(cls, retries: int = 3) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
                sanitized_args = [
                    cls.sanitize_id(arg)
                    if isinstance(arg, (int, str, float)) and str(arg).replace("-", "").isdigit()
                    else arg
                    for arg in args
                ]
                attempt = 0
                while attempt < retries:
                    try:
                        result = func(*sanitized_args, **kwargs)
                        if isinstance(result, str) and ("<html" in result.lower() or "<!doctype" in result.lower()):
                            raise RobloxAPIError("Roblox endpoint returned HTML maintenance payload")
                        return result if isinstance(result, dict) else {"data": result}
                    except (ValueError, RobloxAPIError) as e:
                        attempt += 1
                        if attempt >= retries:
                            return {"success": False, "error": str(e), "attempts": attempt}
                        time.sleep(0.05 * (2 ** attempt))
                    except Exception as fatal:
                        return {"success": False, "error": f"Fatal edge case: {fatal}", "attempts": attempt + 1}
                return {"success": False, "error": "Max retries exceeded", "attempts": retries}
            return wrapper
        return decorator

@RobloxEdgeCaseHandler.safe_api_call(retries=2)
def fetch_place_details(place_id: Union[int, str]) -> Dict[str, Any]:
    if str(place_id) == "999":
        return "<html><body>Roblox Maintenance</body></html>"
    return {"place_id": place_id, "name": "Baseplate", "builder": "Roblox"}
