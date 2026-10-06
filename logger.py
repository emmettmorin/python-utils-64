import logging
import re
from logging.handlers import RotatingFileHandler

COOKIE_PATTERN = re.compile(r"_\|WARNING:-DO-NOT-SHARE-[^\s\"']+")

class RobloxSecurityFilter(logging.Filter):
    """Filters Roblox cookie values from being leaked in logs."""
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = COOKIE_PATTERN.sub("[REDACTED_COOKIE]", record.msg)
        return True

class RobloxStudioFormatter(logging.Formatter):
    """Color-coded console output matching Roblox Studio design schema."""
    COLORS = {
        logging.DEBUG: "\033[94m[DEBUG]\033[0m",
        logging.INFO: "\033[92m[INFO]\033[0m",
        logging.WARNING: "\033[93m[WARN]\033[0m",
        logging.ERROR: "\033[91m[ERROR]\033[0m",
        logging.CRITICAL: "\033[41m[CRIT]\033[0m"
    }

    def format(self, record: logging.LogRecord) -> str:
        prefix = self.COLORS.get(record.levelno, "[LOG]")
        fmt = f"{prefix} %(asctime)s - %(name)s - %(message)s"
        formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def get_logger(name: str, filename: str = "roblox_session.log") -> logging.Logger:
    """Creates a logger with automatic log rotation and Roblox cookie filtering."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(filename, maxBytes=524288, backupCount=3, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter("%(asctime)s