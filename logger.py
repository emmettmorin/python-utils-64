import sys
import datetime
from typing import Any

class RobloxLogger:
    _prefix = '[ROBLOX-64]'
    _colors = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'RESET': '\033[0m'}

    def __init__(self, debug: bool = False):
        self.debug_mode = debug

    def _format(self, level: str, msg: Any) -> str:
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self._colors.get(level, '')
        return f"{color}{self._prefix} [{ts}] {level}: {msg}{self._colors['RESET']}"

    def info(self, msg: Any) -> None:
        print(self._format('INFO', msg))

    def warn(self, msg: Any) -> None:
        print(self._format('WARN', msg), file=sys.stderr)

    def error(self, msg: Any) -> None:
        print(self._format('ERROR', msg), file=sys.stderr)

    def trace(self, msg: Any) -> None:
        if self.debug_mode:
            print(f"{self._prefix} DEBUG: {msg}")

log = RobloxLogger()