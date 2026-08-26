class RobloxUtilsError(Exception):
    """Base exception for all python-utils-64 errors."""
    pass

class InstanceNotFoundError(RobloxUtilsError):
    """Raised when a Roblox Instance cannot be located by path or criteria."""
    def __init__(self, instance_path: str):
        super().__init__(f"Roblox Instance not found at path: {instance_path}")
        self.instance_path = instance_path

class PropertyAccessError(RobloxUtilsError):
    """Raised when a property on a Roblox object cannot be read or written."""
    def __init__(self, property_name: str, reason: str):
        super().__init__(f"Failed to access property '{property_name}': {reason}")
        self.property_name = property_name

class DeserializationError(RobloxUtilsError):
    """Raised when binary or XML model data fails to parse correctly."""
    def __init__(self, offset: int, details: str):
        super().__init__(f"Deserialization failed at offset {offset}: {details}")
        self.offset = offset

class RateLimitExceededError(RobloxUtilsError):
    """Raised when Roblox API requests are throttled."""
    def __init__(self, retry_after: float):
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")
        self.retry_after = retry_after
