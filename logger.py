import logging
import os
import time
from logging.handlers import RotatingFileHandler

class RobloxStudioFormatter(logging.Formatter):
    """Custom formatter providing Luau/Roblox Studio style timestamping and color tags."""
    
    COLORS = {
        logging.DEBUG: "\033[94m[RBX:DBG]\033[0m",
        logging.INFO: "\033[92m[RBX:INF]\033[0m",
        logging.WARNING: "\033[93m[RBX:WRN]\033[0m",
        logging.ERROR: "\033[91m[RBX:ERR]\033[0m",
        logging.CRITICAL: "\033[95m[RBX:CRT]\033[0m"
    }

    def format(self, record: logging.LogRecord) -> str:
        tag = self.COLORS.get(record.levelno, "[RBX:LOG]")
        place_id = getattr(record, "place_id", "Global")
        record.msg = f"{tag} (Place:{place_id}) {record.msg}"
        return super().format(record)


class DynamicPlaceRotatingHandler(RotatingFileHandler):
    """File rotator that shifts log files when size exceeds threshold, stamping timestamp metadata."""
    
    def __init__(self, filename: str, max_bytes: int = 512 * 1024, backup_count: int = 3):
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None
        timestamp = int(time.time())
        dfn = self.rotation_filename(f"{self.baseFilename}.{timestamp}.bak")
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


def setup_roblox_logger(
    name: str = "RobloxUtils",
    log_file: str = "logs/roblox_api.log",
    level: int = logging.INFO,
    max_mb: float = 1.0,
    backups: int = 5
) -> logging.Logger:
    """Configures a rotating logger tuned for Roblox OpenCloud and API operations."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    max_bytes = int(max_mb * 1024 * 1024)
    file_handler = DynamicPlaceRotatingHandler(log_file, max_bytes=max_bytes, backup_count=backups)
    
    fmt = "%(asctime)s %(levelname)s %(message)s"
    formatter = RobloxStudioFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger
