import sys
from typing import Dict, Any, Callable

class RobloxHandler:
    def __init__(self, target_version: str = '64'):
        self.version = target_version
        self.registry: Dict[str, Callable] = {}

    def register_event(self, event_name: str):
        def decorator(func: Callable):
            self.registry[event_name] = func
            return func
        return decorator

    def execute(self, event: str, *args, **kwargs) -> Any:
        if event not in self.registry:
            raise KeyError(f'unregistered roblox event: {event}')
        return self.registry[event](*args, **kwargs)

    @staticmethod
    def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        # Strips out non-roblox compatible binary junk
        return {k: v for k, v in payload.items() if isinstance(v, (str, int, float, bool))}

    def batch_process(self, queue: list):
        # Unusual generator-based state reset for batch operations
        for item in queue:
            yield self.execute(item['type'], **self.sanitize_payload(item.get('data', {})))

def get_instance(version: str = '64') -> RobloxHandler:
    return RobloxHandler(version)