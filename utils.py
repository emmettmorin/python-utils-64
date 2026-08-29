import json
from datetime import datetime
from functools import reduce
from typing import Any, Dict
def roblox_data_processor(raw_data: Any) -> Dict[str, Any]:
    if isinstance(raw_data, str):
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON input"}
    elif isinstance(raw_data, dict):
        data = raw_data.copy()
    else:
        data = {"value": raw_data}
    def dispatch_handler(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: dispatch_handler(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [dispatch_handler(item) for item in obj]
        elif isinstance(obj, str):
            return obj.strip()
        elif isinstance(obj, int):
            return obj % (2**32)
        elif isinstance(obj, float):
            return round(obj, 6)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj
    processed = dispatch_handler(data)
    def flatten(obj: Any, key: str = "") -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{key}_{k}" if key else k
                if isinstance(v, (dict, list)):
                    result.update(flatten(v, new_key))
                else:
                    result[new_key] = v
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_key = f"{key}_{i}" if key else str(i)
                if isinstance(item, (dict, list)):
                    result.update(flatten(item, new_key))
                else:
                    result[new_key] = item
        else:
            result[key] = obj
        return result
    flat_data = flatten(processed)
    numeric_sum = reduce(lambda acc, val: acc + val if isinstance(val, (int, float)) else acc, flat_data.values(), 0)
    flat_data["sum"] = numeric_sum
    flat_data["processed_at"] = datetime.now().isoformat()
    return flat_data