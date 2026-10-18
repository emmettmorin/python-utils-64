import typing

def validate_payload(data: typing.Any) -> bool:
    """Ensures roblox data structure conforms to protocol expectations."""
    if not isinstance(data, dict):
        return False
    
    required_fields = {'place_id', 'user_id', 'payload'}
    if not required_fields.issubset(data.keys()):
        return False
    
    # Roblox-specific sanity checks: IDs should be non-negative
    if data['place_id'] < 0 or data['user_id'] < 0:
        return False

    return True

def sanitize_input(data: dict) -> dict:
    """Forces type safety on incoming network frames."""
    return {
        'place_id': int(data.get('place_id', 0)),
        'user_id': int(data.get('user_id', 0)),
        'payload': str(data.get('payload', '')),
        'timestamp': float(data.get('timestamp', 0.0))
    }

class ValidationError(Exception):
    """Custom error for invalid processing frames."""
    pass

def enforce_frame_schema(frame: typing.Any):
    """Decorator logic for pipeline integrity."""
    if not validate_payload(frame):
        raise ValidationError(f"Malformed payload received: {type(frame)}")
    return sanitize_input(frame)