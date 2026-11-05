import datetime
import inspect
import sys

class RobloxLogger:
    def __init__(self, prefix='[RBX-64]'):
        self.prefix = prefix
        self.colors = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'END': '\033[0m'}

    def _log(self, level, message):
        caller = inspect.stack()[2].function
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        fmt = f"{self.colors.get(level, '')}{self.prefix} {ts} [{level}] ({caller}) -> {message}{self.colors['END']}"
        sys.stdout.write(fmt + '\n')

    def info(self, msg):
        self._log('INFO', msg)

    def warn(self, msg):
        self._log('WARN', msg)

    def error(self, msg):
        self._log('ERROR', msg)

    def __call__(self, *args, **kwargs):
        self.info(' '.join(map(str, args)))

logger = RobloxLogger()