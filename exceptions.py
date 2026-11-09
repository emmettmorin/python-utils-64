class RobloxDataError(Exception):
    """Base exception for data integrity issues."""
    pass

class RobloxSerializationError(RobloxDataError):
    """Raised when data fails Roblox Luau conversion."""
    def __init__(self, key, value, reason):
        self.message = f"Serialization failure at {key} [{type(value).__name__}]: {reason}"
        super().__init__(self.message)

class RobloxRateLimitError(RobloxDataError):
    """Raised when exceeding Roblox API throttle limits."""
    pass

class DataSchemaMismatch(RobloxDataError):
    """Raised when internal dict schema drifts from target."""
    def __init__(self, expected, actual):
        self.message = f"Schema mismatch: expected {expected}, found {actual}"
        super().__init__(self.message)

class LuauTypeMismatch(RobloxDataError):
    """Helper to cast Python types to Luau equivalents."""
    _MAP = {int: 'number', str: 'string', bool: 'boolean', list: 'table', dict: 'table'}

    @staticmethod
    def validate(key, value, expected_type):
        actual = type(value)
        if actual != expected_type:
            raise LuauTypeMismatch(f"Key '{key}' expected {expected_type}, got {actual}")
        return True