import logging
from typing import Dict, Any, Generator, List

logging.basicConfig(level=logging.INFO, format="[RBX-LOG] %(levelname)s - %(message)s")

class RobloxEventLogger:
    ALLOWED_EVENTS = {"PlayerJoin", "PlayerLeave", "PurchaseSuccess", "ExploitDetected"}

    def __init__(self, raw_stream: List[Dict[str, Any]]):
        self.stream = raw_stream
        self.valid_logs: List[Dict[str, Any]] = []

    def _validate_payload(self, payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False
        user_id = payload.get("user_id")
        place_id = payload.get("place_id")
        event = payload.get("event")
        return (
            isinstance(user_id, int) and user_id > 0
            and isinstance(place_id, int) and place_id > 0
            and isinstance(event, str) and event in self.ALLOWED_EVENTS
        )

    def process_log_queue(self) -> Generator[Dict[str, Any], None, None]:
        for idx, log_entry in enumerate(self.stream):
            if not self._validate_payload(log_entry):
                logging.warning(f"Dropping invalid Roblox telemetry at index {idx}: {log_entry}")
                continue
            log_entry["validated_seq"] = idx
            self.valid_logs.append(log_entry)
            logging.info(f"Processed '{log_entry['event']}' for User:{log_entry['user_id']}")
            yield log_entry

if __name__ == "__main__":
    sample_queue = [
        {"user_id": 12345678, "place_id": 987654321, "event": "PlayerJoin"},
        {"user_id": -1, "place_id": 987654321, "event": "PlayerJoin"},
        "invalid_payload",
        {"user_id": 87654321, "place_id": 987654321, "event": "ExploitDetected"},
    ]
    logger_inst = RobloxEventLogger(sample_queue)
    results = list(logger_inst.process_log_queue())
    print(f"Successfully processed {len(results)} valid events.")