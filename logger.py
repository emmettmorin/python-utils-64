import logging
from collections import deque
from datetime import datetime
import json
class RobloxLogger:
    def __init__(self, max_logs=100, log_level=logging.INFO):
        self.max_logs = max_logs
        self.log_buffer = deque(maxlen=max_logs)
        self.logger = logging.getLogger("roblox_utils")
        self.logger.setLevel(log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - ROBLOX - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            file_handler = logging.FileHandler('roblox.log')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    def _log(self, level, message, metadata=None):
        entry = {'time': datetime.utcnow().isoformat(), 'level': level, 'message': message, 'metadata': metadata or {}, 'roblox_context': 'python_utils'}
        self.log_buffer.append(entry)
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(json.dumps(entry))
    def info(self, message, **metadata):
        self._log('INFO', message, metadata)
    def warning(self, message, **metadata):
        self._log('WARNING', message, metadata)
    def error(self, message, **metadata):
        self._log('ERROR', message, metadata)
    def log_player_event(self, player_name, event, details=None):
        meta = {'player': player_name, 'event': event}
        if details:
            meta.update(details)
        self.info(f"Player event for {player_name}: {event}", **meta)
    def get_buffer_contents(self):
        return list(self.log_buffer)
    def export_to_json(self, filename='roblox_logs.json'):
        with open(filename, 'w') as f:
            json.dump(list(self.log_buffer), f, indent=2)
        self.info(f"Exported logs to {filename}")
def create_roblox_logger(max_logs=50):
    return RobloxLogger(max_logs=max_logs)
def log_roblox_action(action_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = RobloxLogger()
            logger.info(f"Starting {action_type}", action=action_type)
            try:
                result = func(*args, **kwargs)
                logger.info(f"Completed {action_type}", result=str(result)[:100])
                return result
            except Exception as e:
                logger.error(f"Failed {action_type}", error=str(e))
                raise
        return wrapper
    return decorator
@log_roblox_action("player_move")
def simulate_player_move(player, direction):
    return f"{player} moved {direction} in Roblox"
if __name__ == "__main__":
    logger = create_roblox_logger(20)
    logger.log_player_event("Builderman", "joined", {"place_id": 1818})
    logger.info("Game initialized", version="64")
    result = simulate_player_move("Noob", "north")
    print("Buffer size:", len(logger.get_buffer_contents()))
    logger.export_to_json()