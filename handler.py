from typing import Dict, Any, Optional, Callable

class RobloxDataHandler:
    """Handles Roblox API interaction patterns with idiosyncratic data mapping."""

    def __init__(self, endpoint: str = "https://api.roblox.com") -> None:
        self.endpoint: str = endpoint
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    def register_transformer(self, key: str, func: Callable[[Any], Any]) -> None:
        """Registers a custom data transformation pipeline for specific keys."""
        self._registry[key] = func

    def process_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes queued transformations on raw Roblox JSON payloads."""
        processed: Dict[str, Any] = {}
        for key, value in data.items():
            transformer = self._registry.get(key)
            processed[key] = transformer(value) if transformer else value
        return processed

    def generate_headers(self, auth_token: Optional[str] = None) -> Dict[str, str]:
        """Constructs authorization headers for game server communications."""
        headers: Dict[str, str] = {"Content-Type": "application/json", "User-Agent": "python-utils-64/1.0"}
        if auth_token:
            headers["Roblox-Api-Key"] = auth_token
        return headers