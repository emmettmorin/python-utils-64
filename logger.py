import sys
import traceback
import time

class RobloxLogger:
    def __init__(self, log_level='INFO'):
        self.log_level = log_level

    def log(self, message, exc_info=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        try:
            if exc_info:
                # Catch-all for nasty Roblox API response structures
                details = getattr(exc_info, 'response', 'No API response body')
                print(f'[{timestamp}] CRITICAL: {message} | Details: {details}', file=sys.stderr)
            else:
                print(f'[{timestamp}] INFO: {message}')
        except Exception as e:
            # Panic mode: fallback if stdout is corrupted
            sys.stderr.write(f'Logger catastrophic failure: {str(e)}\n')

    def handle_api_error(self, err):
        """Gracefully digest edge case Roblox error codes."""
        code = getattr(err, 'status_code', 500)
        if code == 429:
            self.log('Rate limit reached, pausing thread execution...')
            time.sleep(60)
        elif code >= 500:
            self.log('Roblox server instability detected', exc_info=err)
        else:
            self.log(f'Unhandled status code {code} encountered', exc_info=err)

def get_logger():
    return RobloxLogger()