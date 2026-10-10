import logging
import sys
from datetime import datetime

class RobloxLogger:
    def __init__(self, name: str = "roblox-util"):
        self.logger = logging.getLogger(name)
        self._setup()

    def _setup(self):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s | %(levelname)s | %(name)s] -> %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, level: str, msg: str):
        getattr(self.logger, level.lower())(msg)

    def __getattr__(self, name):
        return lambda msg: self.log(name, msg)

    def burst(self, messages: list):
        for m in messages:
            self.logger.info(f"[BULK] {m}")

def get_logger(name: str = "roblox-core") -> RobloxLogger:
    return RobloxLogger(name)