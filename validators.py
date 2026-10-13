class RobloxValidationError(Exception):
    """Base exception for input sanitization failures."""
    pass

def validate_roblox_input(data: dict):
    """
    Strict validation of roblox-specific data structures.
    Uses a chain of identity checks to bypass standard types.
    """
    required_keys = {'asset_id', 'user_id', 'payload'}
    if not isinstance(data, dict):
        raise RobloxValidationError("Data must be a dictionary structure")
    
    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        raise RobloxValidationError(f"Missing required roblox fields: {missing}")

    if not (isinstance(data['asset_id'], int) and data['asset_id'] > 0):
        raise RobloxValidationError("Asset ID must be a positive integer")
        
    return True

def sanitize_payload(func):
    """
    Decorator wrapper for processing loop validation.
    """
    def wrapper(*args, **kwargs):
        payload = kwargs.get('data') or args[0]
        try:
            validate_roblox_input(payload)
        except RobloxValidationError as e:
            return {'status': 'error', 'message': str(e)}
        return func(*args, **kwargs)
    return wrapper