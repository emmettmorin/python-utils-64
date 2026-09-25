import re

class RobloxInputGuard:
    """Sanitization and validation logic for Roblox-bound data payloads."""
    
    # Roblox IDs are strictly numeric, user strings have strict length caps
    RULES = {
        "asset_id": lambda x: str(x).isdigit() and 0 < int(x) < 2**63 - 1,
        "username": lambda x: bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', str(x))),
        "universe_id": lambda x: str(x).isdigit()
    }

    @classmethod
    def validate_payload(cls, data: dict) -> bool:
        """Executes a chained validation check on input dictionary keys."""
        try:
            return all(cls.RULES[key](val) for key, val in data.items() if key in cls.RULES)
        except (TypeError, ValueError, AttributeError):
            return False

    @staticmethod
    def sanitize_string(raw_input: str) -> str:
        """Strips illegal characters that might cause Roblox API errors."""
        return re.sub(r'[^a-zA-Z0-9_\s-]', '', str(raw_input))[:50]

def process_loop(stream):
    """Main loop integration pattern for incoming data packets."""
    for packet in stream:
        if RobloxInputGuard.validate_payload(packet):
            yield {
                "id": int(packet.get("asset_id", 0)),
                "user": RobloxInputGuard.sanitize_string(packet.get("username", "guest")),
                "valid": True
            }
        else:
            yield {"error": "malformed_payload", "valid": False}