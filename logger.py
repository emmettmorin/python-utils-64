import logging
from logging.handlers import RotatingFileHandler
import os

def get_roblox_logger(name='roblox_dev', log_file='dev_session.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s',
            datefmt='%H:%M:%S'
        )

        # Rotator: 5 files, 1MB each - perfect for niche scripts
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024,
            backupCount=5
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Console output for real-time debugging
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Quick access instance for the module
log = get_roblox_logger()