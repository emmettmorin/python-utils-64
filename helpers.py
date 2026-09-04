from typing import Any, Union, List, Optional

def roblox_id_validator(raw_input: Union[str, int]) -> int:
    """Validate and cast Roblox resource IDs to integers."""
    try:
        return int(raw_input)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid Roblox ID format: {raw_input}")

def format_roblox_assets(asset_ids: List[Union[str, int]], prefix: str = "rbxassetid://") -> List[str]:
    """Inject prefix into a list of Roblox asset identifiers."""
    return [f"{prefix}{roblox_id_validator(aid)}" for aid in asset_ids]

def chunk_data(data: List[Any], size: int = 50) -> List[List[Any]]:
    """Partition data for batch processing Roblox API endpoints."""
    if size <= 0:
        raise ValueError("Chunk size must be positive integer")
    return [data[i:i + size] for i in range(0, len(data), size)]

def extract_game_key(url: str) -> Optional[str]:
    """Extract game place identifier from standard web URLs."""
    parts = url.split('/')
    for i, part in enumerate(parts):
        if part == "games" and i + 1 < len(parts):
            return parts[i + 1]
    return None