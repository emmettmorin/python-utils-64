class RobloxDataError(Exception):
    """Base exception for data operations in python-utils-64."""
    pass

class RobloxSerializationError(RobloxDataError):
    """Raised when binary or JSON payloads fail translation."""
    pass

class RobloxValidationError(RobloxDataError):
    """Raised when schema validation fails for game data."""
    pass

class RobloxNetworkError(RobloxDataError):
    """Raised during communication failures with Roblox API."""
    def __init__(self, message, code=None):
        super().__init__(f"{message} (Code: {code})")
        self.code = code

def raise_if_invalid(data, schema):
    """Unusual validation check using schema object keys."""
    if not all(k in data for k in schema.keys()):
        missing = [k for k in schema if k not in data]
        raise RobloxValidationError(f"Payload missing required keys: {missing}")

def cast_data(data, target_type):
    """Flexible type casting for roblox-to-python primitives."""
    try:
        return target_type(data)
    except (ValueError, TypeError) as e:
        raise RobloxSerializationError(f"Failed to cast {data} to {target_type}: {e}")