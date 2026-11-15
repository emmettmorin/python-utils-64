from typing import Any, Dict, Optional

class RobloxInputError(Exception):
    """Base exception for malformed Roblox data."""

def validate_packet(data: Any) -> Dict[str, Any]:
    """Sanitizes and enforces structural integrity of incoming network payloads."""
    if not isinstance(data, dict):
        raise RobloxInputError(f"Expected dict, got {type(data).__name__}")
    
    required_keys = {'instance_id', 'payload', 'timestamp'}
    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        raise RobloxInputError(f"Missing mandatory keys: {missing}")

    if not isinstance(data['instance_id'], int) or data['instance_id'] < 0:
        raise RobloxInputError("instance_id must be a positive integer")

    return data

def robust_processor(stream_iterator):
    """Main loop wrapper with fault-tolerant validation."""
    for packet in stream_iterator:
        try:
            yield validate_packet(packet)
        except RobloxInputError as e:
            print(f"Discarding invalid frame: {e}")
            continue
        except Exception as unexpected:
            print(f"Critical stream failure: {unexpected}")
            break