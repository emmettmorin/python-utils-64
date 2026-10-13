from typing import Dict, Any, Optional, Callable

class RobloxPacketHandler:
    """Handles incoming Roblox WebSocket packets with type-safe routing."""

    def __init__(self) -> None:
        self._routes: Dict[str, Callable[[Dict[str, Any]], None]] = {}

    def register(self, opcode: str) -> Callable[[Callable], Callable]:
        """Decorator for mapping packet opcodes to handler functions."""
        def decorator(func: Callable) -> Callable:
            self._routes[opcode] = func
            return func
        return decorator

    def process(self, packet: Dict[str, Any]) -> Optional[Any]:
        """Routes raw data to the assigned packet handler."""
        opcode: Optional[str] = packet.get("op")
        if opcode and opcode in self._routes:
            return self._routes[opcode](packet.get("data", {}))
        return None

    def __repr__(self) -> str:
        return f"<RobloxPacketHandler routes={list(self._routes.keys())}>"