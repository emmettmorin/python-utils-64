class RobloxInputError(Exception):
    pass

def validate_payload(data: dict) -> bool:
    required_fields = {"asset_id", "user_id", "nonce"}
    if not isinstance(data, dict):
        raise RobloxInputError(f"Payload must be dict, got {type(data).__name__}")
    
    if not required_fields.issubset(data.keys()):
        missing = required_fields - data.keys()
        raise RobloxInputError(f"Missing critical roblox fields: {missing}")
    
    if not isinstance(data.get("asset_id"), int) or data["asset_id"] < 0:
        raise RobloxInputError("Invalid asset_id format")
        
    return True

def robust_parse(raw_data):
    try:
        return validate_payload(raw_data)
    except RobloxInputError as e:
        return False

class DataSanitizer:
    def __init__(self):
        self.telemetry = []

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if args and validate_payload(args[0]):
                return func(*args, **kwargs)
            raise RobloxInputError("Validation sequence integrity compromised")
        return wrapper