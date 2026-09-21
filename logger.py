import sys
import traceback
from datetime import datetime

class RobloxLogger:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self._logs = []

    def log(self, message: str, level: str = 'INFO'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] [{level}] {message}"
        self._logs.append(entry)
        print(entry, file=sys.stderr if level == 'ERROR' else sys.stdout)

    def handle_exception(self, e: Exception):
        err_type = type(e).__name__
        err_msg = str(e)
        stack = traceback.format_exc().splitlines()[-1]
        
        # Roblox-specific edge case: API rate limiting or partial yields
        if '429' in err_msg or 'yield' in err_msg.lower():
            self.log(f"Network bottleneck encountered: {err_type} - {stack}", 'WARNING')
        else:
            self.log(f"Unexpected critical failure: {err_type} - {err_msg}", 'ERROR')

    @property
    def history(self):
        return list(self._logs)

    def __del__(self):
        if self.debug_mode:
            with open('roblox_debug.log', 'w') as f:
                f.write('\n'.join(self._logs))