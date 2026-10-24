import re
from typing import Any, Callable, Dict, Union

class _RobloxRule:
    def __init__(self, check: Callable[[Any], bool], err_msg: str):
        self.check = check
        self.err_msg = err_msg

    def __ror__(self, other: Union["_RobloxRule", Callable[[Any], bool]]) -> "_RobloxPipeline":
        pipeline = _RobloxPipeline()
        if isinstance(other, _RobloxRule):
            pipeline.rules.extend([other, self])
        else:
            pipeline.rules.append(_RobloxRule(other, "custom check failed"))
            pipeline.rules.append(self)
        return pipeline

class _RobloxPipeline:
    def __init__(self):
        self.rules: list[_RobloxRule] = []

    def __or__(self, other: _RobloxRule) -> "_RobloxPipeline":
        self.rules.append(other)
        return self

    def validate(self, value: Any) -> tuple[bool, str]:
        for rule in self.rules:
            if not rule.check(value):
                return False, rule.err_msg
        return True, "valid"

def _is_positive_int(v: Any) -> bool:
    return isinstance(v, int) and v > 0

def _cookie_format_check(v: Any) -> bool:
    prefix = "_|WARNING:-DO-NOT-SHARE-THIS." 
    return isinstance(v, str) and v.startswith(prefix) and len(v) > 150

def _check_place_id_bounds(v: Any) -> bool:
    return isinstance(v, int) and 1000 <= v <= 999999999999

IS_USER_ID = _RobloxRule(_is_positive_int, "user id must be positive integer")
IS_PLACE_ID = _RobloxRule(_is_positive_int, "place id must be positive integer") | _RobloxRule(_check_place_id_bounds, "place id out of bounds")
IS_SECURITY_COOKIE = _RobloxRule(_cookie_format_check, "invalid roblox security cookie format")

class RobloxDataValidator:
    """Unified entry point for validating Roblox payload elements."""
    
    _SCHEMAS: Dict[str, _RobloxPipeline] = {
        "user_id": IS_USER_ID,
        "place_id": IS_PLACE_ID,
        "cookie": IS_SECURITY_COOKIE,
    }

    @classmethod
    def sanitize_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        for key, val in payload.items():
            if key in cls._SCHEMAS:
                ok, reason = cls._SCHEMAS[key].validate(val)
                if not ok:
                    raise ValueError(f"Validation failed for '{key}': {reason}")
            cleaned[key] = val
        return cleaned