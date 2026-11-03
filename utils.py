import json
import re
from typing import Any, Dict, Union

def parse_roblox_id(val: Union[int, str, float]) -> int:
    """Parses and validates a Roblox User/Asset ID with edge-case handling."""
    if val is None:
        raise ValueError("Roblox ID candidate cannot be None")
    
    raw_str = str(val).strip()
    url_match = re.search(r'(?:users|games|catalog|library|places)/(\d+)', raw_str, re.IGNORECASE)
    if url_match:
        raw_str = url_match.group(1)
        
    try:
        num = int(float(raw_str))
    except (ValueError, OverflowError) as err:
        raise ValueError(f"Unparseable Roblox ID candidate: {val}") from err

    if num <= 0:
        raise ValueError(f"Roblox IDs must be positive integers, got: {num}")
    if num > 9_223_372_036_854_775_807:
        raise ValueError(f"Roblox ID exceeds int64 bounds: {num}")

    return num

def sanitize_api_response(response_data: Union[dict, str, bytes]) -> Dict[str, Any]:
    """Edge-case sanitizer for Roblox API responses returning soft errors or raw HTML."""
    if isinstance(response_data, (bytes, bytearray)):
        response_data = response_data.decode("utf-8", errors="replace")
        
    if isinstance(response_data, str):
        cleaned = response_data.strip()
        if not cleaned:
            return {"success": False, "data": None, "error": "empty_response_body"}
        try:
            response_data = json.loads(cleaned)
        except json.JSONDecodeError:
            return {"success": False, "data": None, "error": "html_or_malformed_json"}

    if not isinstance(response_data, dict):
        return {"success": False, "data": response_data, "error": "unexpected_root_type"}

    if "errors" in response_data and isinstance(response_data["errors"], list):
        err_list = response_data["errors"]
        if err_list:
            first_err = err_list[0] if isinstance(err_list[0], dict) else {"message": str(err_list[0])}
            return {
                "success": False,
                "data": response_data,
                "error": first_err.get("message", "unknown_roblox_error"),
                "code": first_err.get("code", -1)
            }

    return {"success": True, "data": response_data, "error": None}
