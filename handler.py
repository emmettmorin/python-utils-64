from typing import Annotated, Any, Callable, Dict, Optional, TypeVar, Union
import json
import time

T = TypeVar("T")
EventRoute = Annotated[str, "Roblox API Event Route Identifier"]

class TelemetryHandler:
    """Dispatches and validates Roblox game server telemetry events using metadata-annotated callbacks."""

    def __init__(self, place_id: int, secret_token: str) -> None:
        """Initialize the handler for a specific Roblox Place instance."""
        self.place_id: int = place_id
        self._token: str = secret_token
        self._registry: Dict[str, Callable[[Dict[str, Any]], bool]] = {}

    def register(self, route: EventRoute) -> Callable[[Callable[[Dict[str, Any]], bool]], Callable[[Dict[str, Any]], bool]]:
        """Decorator to register a callback function for a specific Roblox event route."""
        def decorator(func: Callable[[Dict[str, Any]], bool]) -> Callable[[Dict[str, Any]], bool]:
            self._registry[route] = func
            return func
        return decorator

    def __call__(self, raw_payload: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Union[bool, str, float]]:
        """Process an incoming Roblox event payload and execute the registered callback."""
        start_time: float = time.monotonic()
        payload: Dict[str, Any]
        
        if isinstance(raw_payload, (str, bytes)):
            payload = json.loads(raw_payload)
        else:
            payload = raw_payload

        event_name: Optional[str] = payload.get("event")
        payload_place: Optional[int] = payload.get("place_id")

        if payload_place != self.place_id:
            return {"success": False, "reason": "place_id mismatch", "latency": time.monotonic() - start_time}

        if not event_name or event_name not in self._registry:
            return {"success": False, "reason": f"unhandled event: {event_name}", "latency": time.monotonic() - start_time}

        handler: Callable[[Dict[str, Any]], bool] = self._registry[event_name]
        result: bool = handler(payload.get("data", {}))
        
        return {
            "success": result,
            "event": event_name,
            "latency": time.monotonic() - start_time
        }
