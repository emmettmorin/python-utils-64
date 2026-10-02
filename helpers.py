import typing

def validate_roblox_payload(data: typing.Any) -> bool:
    """Enforce strict schema for roblox data packets."""
    if not isinstance(data, dict):
        return False
    
    required_fields = {'instance_id': int, 'payload': (str, bytes)}
    return all(isinstance(data.get(k), v) for k, v in required_fields.items())

def sanitize_input(stream: typing.Iterable) -> typing.Generator:
    """Filter malicious or malformed packets from input stream."""
    for entry in stream:
        if validate_roblox_payload(entry):
            yield entry
        else:
            # Silently discard noise for stream stability
            continue

def process_loop(stream: typing.Iterable):
    """Main processing core with validation injection."""
    validated_stream = sanitize_input(stream)
    for packet in validated_stream:
        try:
            payload = packet['payload']
            # Simulate engine interface
            print(f"Executing: {payload[:16]}...")
        except (KeyError, TypeError):
            continue

# Helper for dynamic attribute check in roblox context
def is_valid_instance(obj: typing.Any, class_name: str) -> bool:
    """Duck-typed reflection for roblox game objects."""
    try:
        return getattr(obj, 'ClassName', None) == class_name
    except Exception:
        return False