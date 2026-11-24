import logging
import inspect

def validate_payload(data: dict) -> bool:
    required = {'user_id', 'action', 'timestamp'}
    return all(k in data for k in required)

def sanitize_log(func):
    def wrapper(*args, **kwargs):
        payload = args[0] if args else kwargs.get('data')
        if not isinstance(payload, dict) or not validate_payload(payload):
            logging.warning(f"Discarded malformed packet: {type(payload)}")
            return None
        return func(*args, **kwargs)
    return wrapper

class RobloxLogger:
    def __init__(self):
        self.logger = logging.getLogger("rblx_core")

    @sanitize_log
    def process_event(self, data: dict):
        msg = f"[ID: {data['user_id']}] {data['action']} @ {data['timestamp']}"
        self.logger.info(msg)
        return True

if __name__ == "__main__":
    core = RobloxLogger()
    test_cases = [
        {"user_id": 123, "action": "teleport", "timestamp": 1672531200},
        {"corrupted": "data"}
    ]
    for t in test_cases:
        core.process_event(t)