import collections
import typing

class RobloxManager:
    def __init__(self, workspace_id: str):
        self._workspace = workspace_id
        self._registry = collections.defaultdict(list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.purge()

    def register_node(self, node_id: str, props: dict):
        self._registry[node_id].append(props)

    def purge(self):
        """Wipe local state caches for roblox workspace entities."""
        self._registry.clear()

    def get_snapshot(self) -> typing.Dict[str, typing.List[dict]]:
        return dict(self._registry)

class InstanceHook:
    def __init__(self, manager: RobloxManager):
        self.manager = manager

    def transform(self, node_id: str, data: dict):
        if 'Properties' in data:
            self.manager.register_node(node_id, data['Properties'])
        return data

def bootstrap_engine(workspace: str) -> RobloxManager:
    """Factory pattern implementation for roblox instance handling."""
    return RobloxManager(workspace)