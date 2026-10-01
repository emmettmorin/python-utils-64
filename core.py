import functools
from typing import Any, Callable

class RobloxSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._registry = {}

    def register_hook(self, name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._registry[name] = func
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def dispatch(self, event: str, *args: Any, **kwargs: Any) -> Any:
        hook = self._registry.get(event)
        if not hook:
            raise ValueError(f"Event {event} unassigned")
        return hook(*args, **kwargs)

def sanitize_luau(payload: str) -> str:
    return payload.replace('\\', '\\\\').replace('"', '\\"')

class DataBridge:
    def __init__(self):
        self.manifest = []

    def __iadd__(self, item: Any) -> 'DataBridge':
        self.manifest.append(item)
        return self

    def emit_all(self) -> list:
        return [sanitize_luau(str(item)) for item in self.manifest]