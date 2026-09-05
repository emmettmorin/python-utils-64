import re
from typing import Any, Dict, Optional

def validate_roblox_id(id_val: Any) -> bool:
    """Determines if an input follows the standard Roblox ID pattern."""
    return isinstance(id_val, (int, str)) and bool(re.fullmatch(r'\d{5,12}', str(id_val)))

def sanitize_metadata(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive sanitation of dictionary keys and values for API safety."""
    sanitized = {}
    for key, value in data.items():
        clean_key = re.sub(r'[^a-zA-Z0-9_]', '', str(key))
        if isinstance(value, dict):
            sanitized[clean_key] = sanitize_metadata(value)
        elif isinstance(value, (str, int, float, bool)):
            sanitized[clean_key] = value
    return sanitized

def check_datastore_payload(payload: Any) -> Optional[Dict[str, Any]]:
    """Strict schema enforcement for Roblox DataStore service interactions."""
    if not isinstance(payload, dict):
        return None
    
    # Enforce basic constraints on key-value pairs
    output = {}
    for k, v in payload.items():
        if len(str(k)) > 50:
            continue
        output[str(k)] = v
        
    return output if output else None