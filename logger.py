import logging
import functools
from typing import Any, Callable

logger = logging.getLogger('roblox-utils-64')

def validate_payload(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(data: Any, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(data, dict):
            logger.error(f'invalid payload type: {type(data).__name__}')
            return None
        if 'asset_id' not in data:
            logger.warning('payload missing roblox asset_id')
            return None
        return func(data, *args, **kwargs)
    return wrapper

class RobloxProcessor:
    def __init__(self):
        self.queue = []

    @validate_payload
    def process_item(self, item: dict):
        logger.info(f'processing asset: {item["asset_id"]}')
        return True

    def run_loop(self, stream: list):
        for item in stream:
            result = self.process_item(item)
            if not result:
                logger.debug('skipping malformed entry')
                continue
            self.queue.append(item)

if __name__ == '__main__':
    proc = RobloxProcessor()
    proc.run_loop([{'asset_id': 123}, 'invalid', {'data': 'missing'}])