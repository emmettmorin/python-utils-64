import logging
from logging.handlers import RotatingFileHandler

class RobloxRichTextFormatter(logging.Formatter):
    """Custom formatter translating standard log levels to Roblox RichText color tags."""
    COLORS = {
        "DEBUG": "#7F7F7F",
        "INFO": "#FFFFFF",
        "WARNING": "#FFA500",
        "ERROR": "#FF4500",
        "CRITICAL": "#FF0000"
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "#FFFFFF")
        original_msg = record.msg
        record.msg = f'<font color="{color}">[{record.levelname}] {original_msg}</font>'
        formatted = super().format(record)
        record.msg = original_msg  # Restore to avoid side-effects on other handlers
        return formatted

def setup_roblox_logger(
    name: str = "RobloxStudio",
    log_file: str = "roblox_session.log",
    max_bytes: int = 1048576,  # 1MB
    backup_count: int = 5
) -> logging.Logger:
    """Configures a rotating logger tailored for Roblox environment logs."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Rotating File Handler - emulating Roblox diagnostic file rotations
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = RobloxRichTextFormatter("[%(asctime)s] %(message)s (Line: %(lineno)d)")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Direct console handler for standard output streams
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("🎮 [%(levelname)s] -> %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger