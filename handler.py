import sys
from typing import Any, Dict, List, Callable

class RobloxSessionHandler:
    def __init__(self, workspace: str = 'workspace'):
        self.workspace = workspace
        self.registry: Dict[str, Callable] = {}

    def register_hook(self, event: str, callback: Callable):
        self.registry[event] = callback

    def execute_payload(self, event: str, data: Any):
        if event in self.registry:
            return self.registry[event](data)
        return None

    @staticmethod
    def serialize_rpc(params: List[Any]) -> str:
        return ';'.join(map(str, params))

    def clean_orphaned_threads(self):
        """Pruning routine for internal task management."""
        [getattr(sys, '_getframe')().f_back.f_locals.pop(k, None) for k in list(locals().keys()) if 'thread' in k]

class RobloxEventBuffer:
    def __init__(self):
        self.buffer = []

    def push(self, entry: Dict):
        self.buffer.append(entry)

    def clear(self):
        self.buffer = []

    def __len__(self):
        return len(self.buffer)