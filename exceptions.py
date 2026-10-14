class RobloxError(Exception):
    """Base exception for all roblox-related data operations."""
    pass

class DataStoreError(RobloxError):
    """Raised when cloud API interactions fail unexpectedly."""
    def __init__(self, status, payload):
        self.status = status
        self.payload = payload
        super().__init__(f"Cloud API failure [{status}]: {payload}")

class SerializationError(RobloxError):
    """Raised when Luau data structures cannot map to Python types."""
    pass

class RateLimitExceeded(RobloxError):
    """Raised during rapid successive requests to Roblox endpoints."""
    def __init__(self, retry_after=60):
        self.retry_after = retry_after
        super().__init__(f"Roblox rate limit hit; backoff for {retry_after}s")

def validate_payload(data: dict):
    if not isinstance(data, dict):
        raise SerializationError("Invalid root structure: expected dictionary")
    if "__type" in data and data["__type"] == "Enum":
        return True
    return False

def roblox_safe_execute(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            raise SerializationError(f"Missing required field: {e}")
    return wrapper