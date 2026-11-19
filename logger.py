import time
import threading
from collections import deque

class RobloxPerformanceLogger:
    def __init__(self, capacity=1000):
        self._buffer = deque(maxlen=capacity)
        self._lock = threading.Lock()
        self._last_flush = time.perf_counter()

    def log(self, message: str):
        timestamp = time.perf_counter()
        self._buffer.append(f'[{timestamp:.4f}] {message}')
        if timestamp - self._last_flush > 5.0:
            self.flush()

    def flush(self):
        with self._lock:
            batch = list(self._buffer)
            self._buffer.clear()
            self._last_flush = time.perf_counter()
            if batch:
                with open('roblox_perf.log', 'a') as f:
                    f.write('\n'.join(batch) + '\n')

    def __del__(self):
        self.flush()

logger = RobloxPerformanceLogger()