class RobloxError(Exception):
    """Base class for all Roblox-related exceptions."""
    pass

class AssetNotFoundError(RobloxError):
    """Raised when an asset is not found in Roblox."""
    def __init__(self, asset_id: int) -> None:
        super().__init__(f'Asset with ID {asset_id} not found.')
        self.asset_id = asset_id

class PermissionDeniedError(RobloxError):
    """Raised when a user does not have permission to access a resource."""
    pass

class InvalidRequestError(RobloxError):
    """Raised when a request to the Roblox API is invalid."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class RateLimitExceededError(RobloxError):
    """Raised when the API rate limit has been exceeded."""
    pass

# Example usage:
# raise AssetNotFoundError(123456)
# raise InvalidRequestError('Invalid parameters provided for the request.')
