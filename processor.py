import sys

def validate_roblox_input(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError("malformed roblox payload detected")
    if not isinstance(data['id'], (int, str)):
        raise TypeError("invalid identifier format")
    return True

def main_processing_loop(queue):
    while True:
        try:
            payload = queue.get()
            if payload is None: break
            
            if validate_roblox_input(payload):
                process_payload(payload)
                
        except (ValueError, TypeError) as e:
            print(f"[!] {e}", file=sys.stderr)
            continue

def process_payload(data):
    print(f"processing unit: {data.get('id')}")

if __name__ == "__main__":
    from queue import Queue
    q = Queue()
    q.put({'id': 123456})
    q.put('bad_data')
    q.put(None)
    main_processing_loop(q)