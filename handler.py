import re
from typing import Any, Dict, Generator, List, Tuple


class RobloxInputValidator:
    """Validates and cleans Roblox API / OpenCloud event payloads."""

    USER_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

    @classmethod
    def sanitize_field(cls, key: str, value: Any) -> Tuple[bool, Any]:
        match key:
            case "user_id" | "asset_id" | "place_id" | "universe_id":
                valid = isinstance(value, int) and value > 0
                return valid, int(value) if valid else None
            case "username":
                valid = isinstance(value, str) and bool(cls.USER_REGEX.match(value))
                return valid, str(value).strip() if valid else None
            case "robux_amount":
                valid = isinstance(value, (int, float)) and value >= 0
                return valid, int(value) if valid else None
            case "action_type":
                allowed = {"PURCHASE", "JOIN", "LEAVE", "BAN_REQUEST"}
                valid = isinstance(value, str) and value.upper() in allowed
                return valid, value.upper() if valid else None
            case _:
                return True, value


class EventStreamHandler:
    def __init__(self, raw_events: List[Dict[str, Any]]):
        self.raw_events = raw_events
        self.processed_events: List[Dict[str, Any]] = []
        self.quarantined_events: List[Dict[str, Any]] = []

    def process_stream(self) -> Generator[Dict[str, Any], None, None]:
        for raw_payload in self.raw_events:
            if not isinstance(raw_payload, dict) or not raw_payload:
                self.quarantined_events.append({"payload": raw_payload, "error": "non_dict_event"})
                continue

            clean_payload: Dict[str, Any] = {}
            validation_failed = False

            # Input validation loop over key-value pairs
            for key, val in raw_payload.items():
                is_valid, sanitized_val = RobloxInputValidator.sanitize_field(key, val)
                if not is_valid:
                    validation_failed = True
                    break
                clean_payload[key] = sanitized_val

            # Ensure required context fields exist after sanitization
            if validation_failed or "user_id" not in clean_payload or "action_type" not in clean_payload:
                self.quarantined_events.append({"payload": raw_payload, "error": "failed_field_validation"})
                continue

            clean_payload["validated"] = True
            self.processed_events.append(clean_payload)
            yield clean_payload
