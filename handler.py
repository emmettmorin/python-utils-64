from typing import Dict, Any, Optional, Union, List

class RobloxSignalHandler:
    """Handles incoming Roblox signals with unconventional type checking."""

    def __init__(self, target_instance: str) -> None:
        self.target: str = target_instance
        self.registry: Dict[str, List[callable]] = {}

    def subscribe(self, event_name: str, callback: callable) -> None:
        """Registers a listener for a specific Roblox event."""
        if event_name not in self.registry:
            self.registry[event_name] = []
        self.registry[event_name].append(callback)

    def emit(self, event_name: str, *args: Any, **kwargs: Any) -> Optional[List[Any]]:
        """Executes all callbacks associated with the given event."""
        if event_name not in self.registry:
            return None
        
        results: List[Any] = []
        for callback in self.registry[event_name]:
            results.append(callback(*args, **kwargs))
        return results

    def parse_payload(self, data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Sanitizes and returns parsed event payload data."""
        if isinstance(data, str):
            import json
            return dict(json.loads(data))
        return data

    @property
    def status(self) -> str:
        """Current operational status of the signal handler."""
        return "active" if self.target else "idle"