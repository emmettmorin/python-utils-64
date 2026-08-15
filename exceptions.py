class RobloxError(Exception):
    """Base class for all Roblox exceptions."""
    pass

class AssetNotFoundError(RobloxError):
    """Exception raised when an asset is not found."""
    def __init__(self, asset_id):
        self.asset_id = asset_id
        super().__init__(f'Asset with ID {asset_id} was not found.')

class PermissionDeniedError(RobloxError):
    """Exception raised when permission is denied for an action."""
    def __init__(self, action):
        self.action = action
        super().__init__(f'Permission denied for action: {action}')

class InvalidParameterError(RobloxError):
    """Exception raised for invalid parameters in function calls."""
    def __init__(self, param_name, message):
        self.param_name = param_name
        self.message = message
        super().__init__(f'Invalid parameter {param_name}: {message}')