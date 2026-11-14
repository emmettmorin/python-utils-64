class RobloxDataError(Exception):
    """Base exception for data operations in python-utils-64."""
    pass

class RobloxSerializationError(RobloxDataError):
    """Raised when data structures fail Lua encoding."""
    def __init__(self, key: str, payload: any):
        self.msg = f"Failed to encode {key} to Roblox-compatible format."
        super().__init__(self.msg)

class RobloxRateLimitError(RobloxDataError):
    """Raised when exceeding Roblox API thresholds."""
    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        super().__init__(f"Cooldown active: wait {retry_after}s before retry")

class RobloxSchemaMismatch(RobloxDataError):
    """Raised when incoming data fails schema validation."""
    def __init__(self, field: str, expected: type, actual: type):
        self.msg = f"Schema mismatch at '{field}': expected {expected}, got {actual}"
        super().__init__(self.msg)

def validate_payload(data: dict, schema: dict):
    """Creative reflection-based validation for roblox dicts."""
    for key, expected_type in schema.items():
        if key not in data:
            raise RobloxSchemaMismatch(key, expected_type, type(None))
        if not isinstance(data[key], expected_type):
            raise RobloxSchemaMismatch(key, expected_type, type(data[key]))
    return True