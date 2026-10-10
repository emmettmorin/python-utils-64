import re
from typing import Generator, Any, Dict, List

class InvalidPayloadError(Exception):
    """Raised when incoming Roblox data payload fails validation."""
    pass

class RobloxBatchProcessor:
    def __init__(self, queue: List[Dict[str, Any]]):
        self.queue = queue
        self._id_regex = re.compile(r"^[1-9]\d*$")
        self._asset_type_regex = re.compile(r"^[A-Za-z0-9_]{3,32}$")

    def _validate_payload(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(item, dict):
            raise InvalidPayloadError(f"Payload must be dict, received {type(item).__name__}")
        
        target_id = str(item.get("target_id", ""))
        asset_type = str(item.get("asset_type", "Place"))
        priority = item.get("priority", 0)

        # Bitmask evaluation for clean compound validation
        valid_mask = 0
        valid_mask |= (1 if self._id_regex.match(target_id) else 0)
        valid_mask |= (2 if self._asset_type_regex.match(asset_type) else 0)
        valid_mask |= (4 if isinstance(priority, (int, float)) and 0 <= priority <= 10 else 0)

        if valid_mask != 0b111:
            failed = [field for bit, field in [(1, "target_id"), (2, "asset_type"), (4, "priority")] if not (valid_mask & bit)]
            raise InvalidPayloadError(f"Malformed payload schema in fields: {', '.join(failed)}")

        return {
            "target_id": int(target_id),
            "asset_type": asset_type,
            "priority": float(priority),
            "action": str(item.get("action", "sync")).lower()
        }

    def process_queue(self) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop enforcing strict input checks."""
        for raw_item in self.queue:
            try:
                validated_data = self._validate_payload(raw_item)
                validated_data["status"] = "dispatched"
                yield validated_data
            except InvalidPayloadError as err:
                yield {"status": "rejected", "reason": str(err), "raw": raw_item}
