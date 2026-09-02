import json
from typing import Any, Dict, List, Optional, Union

ROBLOX_CONSTANTS = {
    "MAX_USERNAME_LENGTH": 20,
    "MIN_USER_ID": 1,
    "MAX_ASSET_ID": 2**63 - 1,
    "DATASTORE_MAX_KEY_LENGTH": 50,
    "HTTP_TIMEOUT": 30,
    "ASSET_TYPES": {
        1: "Image",
        2: "TShirt",
        3: "Audio",
        4: "Mesh",
        5: "Lua",
        6: "HTML",
        7: "Text",
        8: "Hat",
        9: "Place",
        10: "Model",
        11: "Shirt",
        12: "Pants",
        13: "Decal",
        14: "Avatar",
        15: "Head",
        16: "Face",
        17: "Gear",
        18: "Badge",
        19: "GroupEmblem",
        20: "Animation",
    },
    "VALID_DATA_KEYS": ["id", "name", "displayName", "created", "updated"],
}

def get_constant(name: str) -> Any:
    """Retrieve a Roblox constant by name."""
    return ROBLOX_CONSTANTS.get(name)

def process_roblox_data(raw_data: Union[Dict, List, str]) -> Dict[str, Any]:
    """Utility function to handle and normalize Roblox data structures.
    Creative approach: recursively processes using constant mappings and type checks."""
    if isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "input": raw_data}
    if isinstance(raw_data, dict):
        processed = {}
        for key, value in raw_data.items():
            if key in ROBLOX_CONSTANTS["VALID_DATA_KEYS"]:
                processed[key] = value
            elif key == "assetTypeId":
                asset_map = ROBLOX_CONSTANTS["ASSET_TYPES"]
                processed["assetType"] = asset_map.get(value, "Unknown")
                processed[key] = value
            elif isinstance(value, dict):
                processed[key] = process_roblox_data(value)
            elif isinstance(value, list):
                processed[key] = [process_roblox_data(item) if isinstance(item, (dict, list)) else item for item in value]
            else:
                processed[key] = value
        return processed
    elif isinstance(raw_data, list):
        return [process_roblox_data(item) for item in raw_data]
    return {"data": raw_data}

def validate_roblox_user_id(user_id: int) -> bool:
    """Check if user ID is within Roblox valid range using constants."""
    min_id = ROBLOX_CONSTANTS["MIN_USER_ID"]
    max_id = ROBLOX_CONSTANTS["MAX_ASSET_ID"]
    return min_id <= user_id <= max_id

def batch_handle_roblox_data(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Process multiple data entries in a batch for efficiency."""
    return [process_roblox_data(data) for data in data_list]

def encode_roblox_data(data: Dict[str, Any]) -> str:
    """Unusual encoding: convert data to a Roblox-like string format using json and prefix."""
    processed = process_roblox_data(data)
    return "ROBLOX_DATA:" + json.dumps(processed)