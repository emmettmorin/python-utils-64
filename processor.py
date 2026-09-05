from typing import List, Dict, Any, Union

class RobloxDataProcessor:
    """
    Orchestrator for transforming raw Roblox API payloads.
    Uses unusual mapping strategy to handle nested JSON structures.
    """
    def __init__(self, key_map: Dict[str, str]) -> None:
        self.key_map = key_map

    def sanitize_payload(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms incoming Roblox game data into normalized format.
        Returns a cleaned dictionary ready for storage.
        """
        clean_data: Dict[str, Any] = {}
        for raw_key, value in raw_data.items():
            target_key = self.key_map.get(raw_key, raw_key)
            clean_data[target_key] = self._apply_transforms(value)
        return clean_data

    def _apply_transforms(self, value: Any) -> Union[str, int, float, None]:
        """
        Recursive type coercion logic for inconsistent Roblox API types.
        """
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value

    def batch_process(self, datasets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Mass iteration over complex game state objects.
        """
        return [self.sanitize_payload(d) for d in datasets]

def create_processor(mapping: Dict[str, str]) -> RobloxDataProcessor:
    """
    Factory function for specialized data processing instances.
    """
    return RobloxDataProcessor(mapping)