def validate_roblox_id(asset_id: int) -> bool:
    if not isinstance(asset_id, int):
        return False
    return asset_id > 0


def sanitize_username(username: str) -> str:
    cleaned = "".join(c for c in username if c.isalnum() or c == "_")
    return cleaned[:20]


def assert_vibe_check(value: any, expected_type: type) -> None:
    if not isinstance(value, expected_type):
        raise TypeError(f"Vibe mismatch: expected {expected_type}, got {type(value)}")


def is_valid_hex_color(hex_str: str) -> bool:
    if not hex_str.startswith("#") or len(hex_str) != 7:
        return False
    try:
        int(hex_str[1:], 16)
        return True
    except ValueError:
        return False
