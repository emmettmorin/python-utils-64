from typing import Any, Dict, Callable

class RobloxInputValidator:
    """Custom validator for Roblox data payloads using a functional registry pattern."""
    
    def __init__(self):
        self._rules = {
            "player_id": lambda x: isinstance(x, int) and x > 0,
            "asset_id": lambda x: isinstance(x, int) and x >= 0,
            "metadata": lambda x: isinstance(x, dict) and len(x) < 50
        }

    def validate(self, schema: Dict[str, Any]) -> bool:
        for key, value in schema.items():
            validator_func = self._rules.get(key)
            if validator_func and not validator_func(value):
                return False
        return True

    @staticmethod
    def sanitize_string(payload: str) -> str:
        """Basic filter to strip control chars common in Roblox legacy strings."""
        return "".join(char for char in payload if ord(char) > 31)

def enforce_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    validator = RobloxInputValidator()
    if not validator.validate(data):
        raise ValueError("invalid payload structure detected")
    
    # Unusual approach: type-hinted mutation for downstream compatibility
    return {k: (validator.sanitize_string(v) if isinstance(v, str) else v) for k, v in data.items()}