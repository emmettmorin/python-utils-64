import logging
from logging.handlers import RotatingFileHandler

class RobloxConsoleFormatter(logging.Formatter):
    """Formats log logs to look like Roblox Studio developer console outputs."""
    EMOJIS = {
        logging.DEBUG: "🔘 [DEBUG]",
        logging.INFO: "🟢 [INFO]",
        logging.WARNING: "⚠️ [WARN]",
        logging.ERROR: "🛑 [ERROR]",
        logging.CRITICAL: "💀 [FATAL]"
    }

    def format(self, record):
        log_emoji = self.EMOJIS.get(record.levelno, "📝")
        log_fmt = f"%(asctime)s {log_emoji} %(message)s"
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)

def setup_roblox_logger(file_name: str = "roblox_output.log", limit_bytes: int = 512 * 1024, keeping_count: int = 3):
    """Sets up a standard library logger with size-based log file rotation."""
    logger = logging.getLogger("RobloxLogger")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler(
        file_name, maxBytes=limit_bytes, backupCount=keeping_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(RobloxConsoleFormatter())
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(RobloxConsoleFormatter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger

if __name__ == '__main__':
    log = setup_roblox_logger()
    log.info("Server script environment initialized successfully")
    log.warning("DataStore Request Limit reached; queueing operation")
    log.error("CharacterAppearanceLoaded failed to yield in time")