import logging
from logging.handlers import RotatingFileHandler
import os

def setup_roblox_logger(name: str = "roblox_bot", log_dir: str = "logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # rotating file handler: 5MB limit, keep 3 backups
    path = os.path.join(log_dir, f"{name}.log")
    file_handler = RotatingFileHandler(
        path, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

log = setup_roblox_logger()