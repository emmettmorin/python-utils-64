import sys
from datetime import datetime

class RobloxLogger:
    def __init__(self, tag: str = "ROBLOX-64"):
        self.tag = tag
        self.levels = {"INFO": "[36m", "WARN": "[33m", "ERROR": "[31m"}

    def _format(self, level: str, msg: str) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self.levels.get(level, "[0m")
        return f"{color}[{timestamp}] [{self.tag}] [{level}]: {msg}[0m"

    def log(self, level: str, message: str):
        formatted = self._format(level.upper(), message)
        stream = sys.stderr if level == "ERROR" else sys.stdout
        print(formatted, file=stream)

    def info(self, msg: str): self.log("INFO", msg)
    def warn(self, msg: str): self.log("WARN", msg)
    def error(self, msg: str): self.log("ERROR", msg)

    def __call__(self, *args):
        self.info(" ".join(map(str, args)))

def create_logger(tag: str = "ROBLOX-64") -> RobloxLogger:
    return RobloxLogger(tag)

if __name__ == "__main__":
    logger = create_logger()
    logger.info("service heartbeat initialized")
    logger("shorthand log injection test")