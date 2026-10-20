from typing import Any, Callable, Dict

class RobloxInputError(Exception):
    """Custom error for invalid Roblox API inputs."""
    pass

def validate_payload(payload: Any, schema: Dict[str, type]) -> bool:
    """Validates dictionary keys and types for roblox payloads."""
    if not isinstance(payload, dict):
        raise RobloxInputError("Payload must be a dictionary structure")
    
    for key, expected_type in schema.items():
        if key not in payload:
            raise RobloxInputError(f"Missing required field: {key}")
        if not isinstance(payload[key], expected_type):
            raise RobloxInputError(f"Field {key} expected {expected_type}, got {type(payload[key])}")
    return True

def sanitize_input(func: Callable) -> Callable:
    """Decorator pattern for wrapping core processing calls."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RobloxInputError as e:
            return {"status": "error", "message": str(e)}
    return wrapper

class InputValidator:
    """Validator orchestrator for processing loops."""
    def __init__(self):
        self.registry = {}

    def register_schema(self, event_type: str, schema: Dict[str, type]):
        self.registry[event_type] = schema

    def check(self, event_type: str, data: Any):
        if event_type not in self.registry:
            return False
        return validate_payload(data, self.registry[event_type])