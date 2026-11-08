import json
import math
from typing import Any, Dict, Union, Callable

class RobloxAssetError(Exception):
    """Base exception for Roblox asset processing failures."""
    pass

class CorruptPayloadError(RobloxAssetError):
    """Raised when asset payload structure is unparseable."""
    pass

class EdgeCaseGuard:
    """Contextual decorator mapping specific edge cases to fallback values."""

    def __init__(self, fallback: Any = None, catch_errs: tuple = (ValueError, TypeError, KeyError)):
        self.fallback = fallback
        self.catch_errs = catch_errs

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except self.catch_errs as err:
                if callable(self.fallback):
                    return self.fallback(err, *args, **kwargs)
                return self.fallback
        return wrapper

class AssetProcessor:
    """Processes raw Roblox place and asset data with edge-case resistance."""

    @staticmethod
    @EdgeCaseGuard(fallback=0)
    def sanitize_asset_id(raw_id: Union[int, str, float]) -> int:
        """Normalizes Roblox asset IDs, safely deflecting negative, float, or overflow cases."""
        if isinstance(raw_id, float) and (math.isnan(raw_id) or math.isinf(raw_id)):
            return 0
        val = int(abs(float(raw_id)))
        return 0 if val > (2**63 - 1) else val

    @staticmethod
    def parse_vector3(data: Dict[str, Union[int, float]]) -> Dict[str, float]:
        """Extracts Vector3 coordinates, guarding against missing axes or non-numeric values."""
        coords = {}
        for axis in ("X", "Y", "Z"):
            val = data.get(axis, 0.0)
            try:
                num_val = float(val)
                coords[axis] = 0.0 if math.isnan(num_val) or math.isinf(num_val) else num_val
            except (ValueError, TypeError):
                coords[axis] = 0.0
        return coords

    @classmethod
    def safe_load_datastore_payload(cls, raw_data: Union[str, bytes, dict]) -> Dict[str, Any]:
        """Parses Datastore payloads, resolving byte wrappers and corrupt JSON edges."""
        if isinstance(raw_data, dict):
            return raw_data
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8", errors="ignore")

        if not raw_data or not str(raw_data).strip():
            return {}

        try:
            parsed = json.loads(raw_data)
            return parsed if isinstance(parsed, dict) else {"raw_value": parsed}
        except json.JSONDecodeError as exc:
            cleaned = str(raw_data).replace("'", '"')
            try:
                return json.loads(cleaned)
            except Exception:
                raise CorruptPayloadError(f"Malformed Roblox datastore payload at byte {exc.pos}")