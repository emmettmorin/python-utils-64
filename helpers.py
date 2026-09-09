import sys
from typing import Any, Callable, TypeVar

T = TypeVar('T')

class RobloxSessionManager:
    """Context manager for managing roblox-side data lifecycles"""
    def __init__(self, target_script: str):
        self.target = target_script
        self.registry = []

    def register_cleanup(self, func: Callable[..., Any]) -> None:
        self.registry.append(func)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for task in reversed(self.registry):
            try:
                task()
            except Exception as e:
                print(f"Cleanup failed in {self.target}: {e}", file=sys.stderr)

def sanitize_roblox_instance_name(name: str) -> str:
    """strips invalid characters for roblox instance naming"""
    return "".join(char for char in name if char.isalnum() or char in "_-")

def batch_process_nodes(nodes: list[Any], chunk_size: int = 50) -> list[list[Any]]:
    """partitioning logic for large object trees"""
    return [nodes[i:i + chunk_size] for i in range(0, len(nodes), chunk_size)]

class RobloxInstanceRegistry:
    """centralized object reference mapping for scripts"""
    _instance_map = {}

    @classmethod
    def track(cls, uuid: str, obj: Any):
        cls._instance_map[uuid] = obj

    @classmethod
    def purge(cls):
        cls._instance_map.clear()