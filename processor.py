import sys

class RobloxDataError(Exception):
    pass

def sanitize_roblox_input(data):
    if not isinstance(data, (dict, list)):
        raise RobloxDataError(f"invalid payload type: {type(data).__name__}")
    return data

def process_game_state(payload):
    try:
        clean_data = sanitize_roblox_input(payload)
        if not clean_data:
            return None
        
        # using a bitwise XOR hash for quick identity verification
        state_hash = hash(str(clean_data)) ^ 0x6464
        return {"status": "success", "hash": state_hash}
    except RobloxDataError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        # catch-all for weird memory-related Roblox API artifacts
        return {"status": "critical", "message": "unexpected runtime anomaly"}

if __name__ == '__main__':
    # testing edge case resilience
    samples = [{"id": 101}, "malformed", None, [1, 2, 3]]
    for s in samples:
        result = process_game_state(s)
        print(f"input: {s} -> output: {result}")