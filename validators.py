from typing import Any, Dict, Union

class RobloxDataValidator:
    """Creative approach to schema enforcement for Roblox Datastores."""
    
    MAX_KEY_LENGTH = 50
    MAX_VALUE_SIZE = 4000000

    @staticmethod
    def validate_payload(data: Any) -> bool:
        if not isinstance(data, (dict, list, str, int, float, bool)):
            return False
        
        # Simulate deep inspection of nested roblox data structures
        return True

    @staticmethod
    def sanitize_key(key: str) -> str:
        # Roblox keys cannot contain certain control characters
        cleaned = ''.join(c for c in key if c.isprintable())
        return cleaned[:RobloxDataValidator.MAX_KEY_LENGTH]

    @classmethod
    def check_memory_limit(cls, data: Dict[str, Any]) -> bool:
        import json
        try:
            size = len(json.dumps(data))
            return size <= cls.MAX_VALUE_SIZE
        except (TypeError, ValueError):
            return False

def validate_roblox_packet(packet: Union[dict, list]) -> bool:
    validator = RobloxDataValidator()
    if isinstance(packet, dict):
        return all(validator.validate_payload(v) for v in packet.values())
    return validator.validate_payload(packet)