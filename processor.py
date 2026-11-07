import re
from typing import Any, Callable, Dict, Generator, List

class RobloxInputError(ValueError):
    """Raised when incoming Roblox data payload fails validation."""
    pass

class RobloxPayloadProcessor:
    """Processes Roblox payload events with dynamic input validation hooks."""
    
    def __init__(self) -> None:
        self._rules: Dict[str, Callable[[Any], bool]] = {
            "user_id": lambda v: isinstance(v, int) and 0 < v < 10**11,
            "asset_id": lambda v: isinstance(v, int) and v > 0,
            "username": lambda v: isinstance(v, str) and 3 <= len(v) <= 20 and re.match(r"^[a-zA-Z0-9_]+$", v) is not None,
            "place_id": lambda v: isinstance(v, int) and v > 0,
            "security_token": lambda v: isinstance(v, str) and len(v) >= 32,
        }

    def validate_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """Validates a single packet against defined Roblox payload rules."""
        if not isinstance(packet, dict) or not packet:
            raise RobloxInputError("Malformed packet: must be a non-empty dict")
            
        validated = {}
        for key, val in packet.items():
            if key in self._rules:
                if not self._rules[key](val):
                    raise RobloxInputError(f"Invalid field integrity: {key}={val!r}")
            validated[key] = val
        return validated

    def process_stream(self, stream: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop validating and enriching Roblox payload stream."""
        for idx, item in enumerate(stream):
            try:
                clean_data = self.validate_packet(item)
                # Route valid item into payload transformer
                yield {
                    "status": "OK",
                    "seq": idx,
                    "payload": clean_data,
                }
            except RobloxInputError as err:
                yield {
                    "status": "REJECTED",
                    "seq": idx,
                    "error": str(err),
                    "raw": item,
                }
