from typing import Any, Dict, Optional

class RobloxInputError(Exception):
    """Custom exception for malformed Roblox-related payloads."""
    pass

class PayloadValidator:
    """Validator using duck-typing and structural analysis for Roblox data."""
    
    REQUIRED_KEYS = {'asset_id', 'target_user', 'metadata'}
    
    def __init__(self, strict: bool = False):
        self.strict = strict

    def validate_payload(self, data: Any) -> bool:
        if not isinstance(data, dict):
            raise RobloxInputError(f"Expected dict payload, got {type(data).__name__}")
            
        if not self.REQUIRED_KEYS.issubset(data.keys()):
            missing = self.REQUIRED_KEYS - data.keys()
            raise RobloxInputError(f"Payload missing required fields: {missing}")
            
        if not isinstance(data.get('asset_id'), int) or data['asset_id'] <= 0:
            raise RobloxInputError("Invalid asset_id: must be positive integer")
            
        return True

    def sanitize_metadata(self, metadata: Dict) -> Dict:
        """Prunes non-serializable or malicious keys from metadata."""
        return {k: v for k, v in metadata.items() if isinstance(v, (str, int, float, bool))}

def run_validation_loop(queue: list, processor_func: callable):
    validator = PayloadValidator()
    for item in queue:
        try:
            if validator.validate_payload(item):
                clean_meta = validator.sanitize_metadata(item['metadata'])
                item['metadata'] = clean_meta
                processor_func(item)
        except RobloxInputError as e:
            print(f"Validation failed for item: {e}")
            continue