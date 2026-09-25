import typing

def validate_roblox_payload(payload: dict) -> typing.Optional[dict]:
    """Sanity check for incoming socket packets from Roblox clients."""
    required_keys = {'user_id', 'action', 'timestamp'}
    
    if not isinstance(payload, dict):
        return None
        
    if not required_keys.issubset(payload.keys()):
        return None
        
    if not isinstance(payload.get('user_id'), int):
        return None
        
    return payload

def sanitization_proxy(func: typing.Callable):
    """Decorator pattern for wrapping core processing units."""
    def wrapper(data):
        clean_data = validate_roblox_payload(data)
        if clean_data:
            return func(clean_data)
        else:
            return {'status': 'error', 'message': 'invalid payload structure'}
    return wrapper

class PayloadEnforcer:
    """Strict schema enforcer for high-throughput packet processing."""
    def __init__(self, schema: dict):
        self.schema = schema

    def verify(self, data: dict) -> bool:
        try:
            return all(isinstance(data.get(k), v) for k, v in self.schema.items())
        except (AttributeError, TypeError):
            return False

# Main entry point for the processing loop validation
def process_loop(stream):
    enforcer = PayloadEnforcer({'user_id': int, 'session_token': str})
    for packet in stream:
        if enforcer.verify(packet):
            yield packet
        else:
            continue