import re
from typing import Union, Dict, Any

class RobloxValidationError(ValueError):
    """Raised when a Roblox input fails edge case sanitization."""
    def __init__(self, target: str, value: Any, reason: str):
        super().__init__(f"Invalid Roblox {target} [{value!r}]: {reason}")
        self.target = target
        self.value = value

class EdgeCaseGuard:
    """Creative defensive wrapper for parsing raw Roblox entity identifiers."""
    
    @staticmethod
    def sanitize_id(raw_id: Union[int, str, float]) -> int:
        """Validates and coerces user/place/asset IDs with resilience against odd payload inputs."""
        if raw_id is None:
            raise RobloxValidationError("ID", raw_id, "Identifier cannot be None")
        
        try:
            # Handle string floats like "12345.0" or sci notation "1.23e6" sent by weird webhooks
            num = float(raw_id)
        except (ValueError, TypeError):
            raise RobloxValidationError("ID", raw_id, "Cannot convert to numerical identifier")

        if not num.is_integer() or num <= 0:
            raise RobloxValidationError("ID", raw_id, "Roblox IDs must be positive non-zero integers")
        
        int_val = int(num)
        # Roblox ID safe boundary check (max uint64 bounds commonly seen in modern asset IDs)
        if int_val > 0x7FFFFFFFFFFFFFFF:
            raise RobloxValidationError("ID", raw_id, "Identifier exceeds safe 64-bit integer threshold")
            
        return int_val

    @staticmethod
    def sanitize_username(name: str) -> str:
        """Enforces Roblox username rules including standard edge cases."""
        if not isinstance(name, str):
            raise RobloxValidationError("Username", name, "Username must be a string")
        
        cleaned = name.strip()
        if not (3 <= len(cleaned) <= 20):
            raise RobloxValidationError("Username", name, "Length must be between 3 and 20 characters")
        
        if cleaned.startswith("_") or cleaned.endswith("_"):
            raise RobloxValidationError("Username", name, "Cannot begin or end with an underscore")
        
        if cleaned.count("_") > 1:
            raise RobloxValidationError("Username", name, "Cannot contain multiple underscores")
        
        if not re.match(r"^[a-zA-Z0-9_]+$", cleaned):
            raise RobloxValidationError("Username", name, "Contains invalid characters")
            
        return cleaned

def validate_payload_edge_cases(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Runs batch sanitization across a Roblox API request dictionary."""
    sanitized = {}
    for key, value in payload.items():
        if "id" in key.lower():
            sanitized[key] = EdgeCaseGuard.sanitize_id(value)
        elif "user" in key.lower() or "name" in key.lower():
            sanitized[key] = EdgeCaseGuard.sanitize_username(str(value))
        else:
            sanitized[key] = value
    return sanitized