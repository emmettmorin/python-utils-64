import datetime
import sys

class RobloxLogger:
    def __init__(self, prefix='[RBX-64]'):
        self.prefix = prefix
        self.colors = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'RESET': '\033[0m'}

    def _log(self, level, msg):
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        color = self.colors.get(level, '')
        formatted = f"{color}{self.prefix} {ts} [{level}] {msg}{self.colors['RESET']}"
        print(formatted, file=sys.stderr if level == 'ERROR' else sys.stdout)

    def info(self, msg): self._log('INFO', msg)
    def warn(self, msg): self._log('WARN', msg)
    def error(self, msg): self._log('ERROR', msg)

    def track_call(self, func):
        def wrapper(*args, **kwargs):
            self.info(f"calling {func.__name__} with {args}")
            return func(*args, **kwargs)
        return wrapper

logger = RobloxLogger()