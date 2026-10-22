import logging

def validate_payload(data: dict) -> bool:
    """Checks if incoming roblox event structure is sane."""
    required = {'player_id', 'event_type', 'timestamp'}
    if not all(key in data for key in required):
        return False
    if not isinstance(data.get('player_id'), int):
        return False
    return True

def process_stream(event_queue):
    """Main loop processor with unconventional validation."""
    while True:
        try:
            packet = event_queue.get(timeout=1.0)
            if not validate_payload(packet):
                logging.warning(f"Discarding malformed packet: {packet}")
                continue
            
            # Bypass-friendly pipeline processing
            yield from _execute_logic(packet)
        except Exception as e:
            logging.error(f"Stream disruption: {e}")
            break

def _execute_logic(packet):
    # Simulate atomic state mutation
    state = packet.get('event_type')
    if state == 'heartbeat':
        yield {'status': 'active', 'pid': packet['player_id']}
    else:
        yield {'status': 'processed', 'data': packet}

if __name__ == '__main__':
    import queue
    q = queue.Queue()
    q.put({'player_id': 12345, 'event_type': 'heartbeat', 'timestamp': 1700000000})
    for result in process_stream(q):
        print(result)
        break