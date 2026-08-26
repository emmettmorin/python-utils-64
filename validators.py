from typing import Any, Dict, List, Union

class RobloxDataError(ValueError):
    pass

def sanitize_roblox_key(key: Any) -> str:
    if not isinstance(key, (str, int)):
        raise RobloxDataError(f"Invalid key type: {type(key)}. Must be string or int.")
    
    str_key = str(key)
    if len(str_key) > 50:
        raise RobloxDataError("Key exceeds Roblox maximum length of 50 characters.")
    
    if not str_key.isprintable() or any(c in str_key for c in ".$\"/\\"):
        raise RobloxDataError(f"Key contains forbidden Roblox characters: {str_key}")
        
    return str_key

def validate_datastore_payload(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        try:
            payload = dict(payload)
        except (TypeError, ValueError):
            raise RobloxDataError("Payload must be a mapping or convertible to dict.")
            
    sanitized: Dict[str, Any] = {}
    for k, v in payload.items():
        clean_key = sanitize_roblox_key(k)
        if isinstance(v, (dict, list)):
            sanitized[clean_key] = validate_datastore_payload(v) if isinstance(v, dict) else [str(i) for i in v]
        elif isinstance(v, (str, int, float, bool, type(None))):
            sanitized[clean_key] = v
        else:
            raise RobloxDataError(f"Unsupported value type for Roblox DataStore: {type(v)}")
            
    return sanitized
