import json
import re
from typing import Any, Dict

class RobloxParseError(Exception):
    pass

def handle_roblox_edge_cases(data: Any) -> Dict[str, Any]:
    result = {"status": "success", "data": {}}
    try:
        if data is None:
            raise ValueError("No data provided")
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                numbers = re.findall(r'-?\d+\.?\d*', data)
                if numbers:
                    data = {"extracted_values": [float(n) if '.' in n else int(n) for n in numbers]}
                else:
                    raise RobloxParseError("Unparseable data")
        if not isinstance(data, dict):
            data = {"items": data} if isinstance(data, (list, tuple)) else {"value": data}
        user_id = data.get("userId") or data.get("id")
        if user_id is None:
            data["userId"] = 1
        else:
            try:
                uid = int(user_id)
                data["userId"] = abs(uid) or 1
            except (ValueError, TypeError):
                data["userId"] = 1
        stats = data.get("stats", {})
        if not isinstance(stats, dict):
            stats = {}
        cleaned = {}
        for k, v in stats.items():
            try:
                cleaned[k] = max(0, float(v)) if isinstance(v, (int, float)) else 0.0
            except:
                cleaned[k] = 0.0
        data["stats"] = cleaned
        if "playtime" in cleaned and "games" in cleaned and cleaned.get("games", 0) > 0:
            try:
                data["avg_playtime"] = cleaned["playtime"] / cleaned["games"]
            except:
                data["avg_playtime"] = 0.0
        result["data"] = data
    except RobloxParseError as e:
        result = {"status": "error", "error": str(e)}
    except Exception as e:
        result = {"status": "fallback", "error": type(e).__name__, "data": {"userId": 1, "stats": {}}}
    return result