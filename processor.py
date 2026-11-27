import logging

class RobloxDataError(Exception):
    pass

def sanitize_roblox_input(data):
    if not isinstance(data, (dict, list)):
        raise RobloxDataError(f"invalid payload type: {type(data).__name__}")
    return data

def process_game_state(payload):
    try:
        clean_data = sanitize_roblox_input(payload)
        if 'place_id' not in clean_data:
            raise KeyError('missing mandatory roblox field: place_id')
        return {"status": "ok", "id": clean_data['place_id']}
    except (RobloxDataError, KeyError) as e:
        logging.error(f"roblox pipeline failure: {e}")
        return {"status": "failed", "error": str(e)}
    except Exception as unexpected:
        logging.critical(f"unexpected engine collapse: {unexpected}")
        return {"status": "fatal"}

if __name__ == '__main__':
    mock = {'place_id': 12345}
    print(process_game_state(mock))