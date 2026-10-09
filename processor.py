from typing import List, Dict, Any, Union, Optional

class RobloxDataProcessor:
    """Utility for transforming Roblox API payloads into internal structures."""

    def __init__(self, raw_data: List[Dict[str, Any]]) -> None:
        self.data = raw_data

    def extract_ids(self, key: str = "id") -> List[int]:
        """Extract unique asset IDs using list comprehension trickery."""
        return list({int(item[key]) for item in self.data if key in item})

    def sanitize_metadata(self, fields: List[str]) -> List[Dict[str, Any]]:
        """Prune sensitive metadata keys from game instance data."""
        return [{k: v for k, v in obj.items() if k not in fields} for obj in self.data]

    def batch_process(self, transform_func: callable) -> List[Any]:
        """Apply custom transformation function to current data set."""
        return [transform_func(item) for item in self.data]

    @property
    def count(self) -> int:
        """Return the current quantity of processed items."""
        return len(self.data)

def initialize_processor(payload: List[Dict[str, Any]]) -> RobloxDataProcessor:
    """Factory function for creating processor instances with type enforcement."""
    return RobloxDataProcessor(payload)