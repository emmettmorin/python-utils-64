import time
import collections
import functools

class RobloxLogger:
    """High-performance ring buffer logging for Roblox API streams."""
    def __init__(self, capacity=1000):
        self._buffer = collections.deque(maxlen=capacity)
        self._last_flush = time.monotonic()
        self._batch_threshold = 0.5

    def log(self, message: str, level: str = "INFO") -> None:
        timestamp = time.monotonic()
        entry = f"[{timestamp:.4f}] {level}: {message}"
        self._buffer.append(entry)
        
        if timestamp - self._last_flush > self._batch_threshold:
            self.flush()

    def flush(self) -> None:
        if not self._buffer:
            return
        
        data = "\n".join(list(self._buffer))
        try:
            with open("roblox_core.log", "a") as f:
                f.write(data + "\n")
            self._buffer.clear()
            self._last_flush = time.monotonic()
        except OSError:
            pass

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log(f"Error in {func.__name__}: {str(e)}", "CRITICAL")
                raise
        return wrapper

logger = RobloxLogger()