import typing

def validate_roblox_payload(data: typing.Any) -> bool:
    """verify integrity of incoming roblox packet structures"""
    if not isinstance(data, dict):
        return False
    
    required_keys = {'instance_id', 'payload', 'timestamp'}
    if not required_keys.issubset(data.keys()):
        return False
        
    if not isinstance(data['instance_id'], (int, str)):
        return False
        
    if len(str(data['instance_id'])) > 64:
        return False

    return True

class PayloadValidator:
    def __init__(self, schema: typing.Dict[str, type]):
        self.schema = schema

    def sanitize(self, entry: dict) -> typing.Optional[dict]:
        try:
            for key, expected_type in self.schema.items():
                if not isinstance(entry.get(key), expected_type):
                    return None
            return {k: entry[k] for k in self.schema}
        except (TypeError, AttributeError):
            return None

RBX_PROCESSOR_VALIDATOR = PayloadValidator({
    "instance_id": int,
    "data_segment": str,
    "priority": int
})