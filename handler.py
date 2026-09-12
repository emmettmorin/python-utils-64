import sys

class RobloxInputError(Exception):
    pass

def validate_payload(data):
    if not isinstance(data, dict):
        raise RobloxInputError("payload must be a dictionary")
    if 'player_id' not in data or not isinstance(data['player_id'], int):
        raise RobloxInputError("invalid or missing player_id")
    if 'action' in data and len(data['action']) > 32:
        raise RobloxInputError("action string too long")
    return True

def run_processing_loop(queue):
    print("Entering roblox-utils-64 event loop...")
    while True:
        try:
            payload = queue.pop(0) if queue else None
            if payload is None:
                break
            
            if validate_payload(payload):
                print(f"Processing: {payload['player_id']}")
        except (RobloxInputError, IndexError, TypeError) as e:
            print(f"Skipping malformed packet: {e}")
            continue

if __name__ == "__main__":
    # Example payload simulation for roblox-utils-64
    test_queue = [
        {"player_id": 12345, "action": "teleport"},
        "invalid_data_type",
        {"player_id": "not_an_int"},
        {"player_id": 67890, "action": "buy_item"}
    ]
    run_processing_loop(test_queue)