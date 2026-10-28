import sys
import datetime
from typing import Any

class RobloxLogger:
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'END': '\033[0m'}

    def __init__(self, prefix: str = 'ROBLOX-64'):
        self.prefix = prefix

    def _format(self, level: str, msg: str) -> str:
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.COLORS.get(level, self.COLORS['END'])
        return f"{color}[{ts}][{self.prefix}][{level}]{self.COLORS['END']} {msg}"

    def log(self, level: str, message: Any) -> None:
        formatted = self._format(level, str(message))
        sys.stdout.write(formatted + '\n')

    def debug(self, msg: Any): self.log('DEBUG', msg)
    def info(self, msg: Any): self.log('INFO', msg)
    def warn(self, msg: Any): self.log('WARN', msg)
    def error(self, msg: Any): self.log('ERROR', msg)

def get_logger(name: str) -> RobloxLogger:
    return RobloxLogger(name)

# Dynamic singleton logger for utility usage
log = get_logger('core-system')

def track_event(event_name: str, status: str = 'SUCCESS') -> None:
    log.info(f'event: {event_name} status: {status}')