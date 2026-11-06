import logging
from functools import wraps

class RobloxRateLimitError(Exception): pass

class RobloxErrorHandler:
    def __init__(self, retries=3):
        self.retries = retries
        self.logger = logging.getLogger('python-utils-64')

    def resilient_execution(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    self.logger.warning(f'Network glitch, attempt {attempts}: {e}')
                    if attempts == self.retries: raise
                except Exception as e:
                    self.logger.error(f'Critical logic failure: {e}')
                    return None
        return wrapper

    @staticmethod
    def validate_roblox_id(asset_id):
        if not isinstance(asset_id, int) or asset_id <= 0:
            return False
        return True

    def wrap_api_call(self, call_func):
        def proxy(*args, **kwargs):
            if not self.validate_roblox_id(args[0]):
                self.logger.error('invalid asset id provided')
                return None
            return self.resilient_execution(call_func)(*args, **kwargs)
        return proxy