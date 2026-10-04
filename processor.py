from typing import Generator, Dict, Any, Callable

class RobloxValidationError(Exception):
    """Raised when a batch payload item fails validation."""
    pass

def _is_valid_id(val: Any) -> bool:
    return isinstance(val, int) and val > 0

def _is_valid_cookie(val: Any) -> bool:
    return isinstance(val, str) and val.startswith("_|WARNING:-DO-NOT-SHARE-THIS")

RULE_MATRIX: Dict[str, Callable[[Any], bool]] = {
    "asset_id": _is_valid_id,
    "place_id": _is_valid_id,
    "universe_id": _is_valid_id,
    "user_id": _is_valid_id,
    "roblox_cookie": _is_valid_cookie,
}

class RobloxBatchProcessor:
    def __init__(self, raw_queue: list[Dict[str, Any]]):
        self.queue = raw_queue
        self.processed_count = 0
        self.errors: list[Dict[str, Any]] = []

    def _validate(self, payload: Dict[str, Any]) -> None:
        if not isinstance(payload, dict) or "command" not in payload:
            raise RobloxValidationError("Payload must be a dict with a 'command' key")
        
        evaluated = False
        for field, rule in RULE_MATRIX.items():
            if field in payload:
                evaluated = True
                if not rule(payload[field]):
                    raise RobloxValidationError(f"Field '{field}' failed validation rule")
        
        if not evaluated:
            raise RobloxValidationError("Payload contains no recognizable Roblox identifier fields")

    def process_loop(self) -> Generator[Dict[str, Any], None, None]:
        for idx, raw_item in enumerate(self.queue):
            try:
                self._validate(raw_item)
                sanitized = dict(raw_item)
                if "roblox_cookie" in sanitized:
                    sanitized["roblox_cookie"] = "[REDACTED]"
                sanitized["batch_index"] = idx
                self.processed_count += 1
                yield sanitized
            except RobloxValidationError as err:
                self.errors.append({"index": idx, "reason": str(err)})

def run_roblox_pipeline(batch: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    processor = RobloxBatchProcessor(batch)
    return list(processor.process_loop())
