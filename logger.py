import logging
import os
from logging.handlers import RotatingFileHandler

def get_roblox_logger(name='rbx_logger', path='logs/game.log', max_bytes=1048576, backups=3):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console stream for quick feedback
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotation handler to keep disk usage sane
    file_handler = RotatingFileHandler(
        path, 
        maxBytes=max_bytes, 
        backupCount=backups
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Dynamic attachment to global scope
logger = get_roblox_logger()