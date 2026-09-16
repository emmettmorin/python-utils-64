import logging
from logging.handlers import RotatingFileHandler
import os

def get_roblox_logger(name='rbx-utils', path='logs/dev.log'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s >>> %(message)s',
        datefmt='%H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        path, maxBytes=1024 * 1024 * 5, backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Roblox-centric quick accessor
class RobloxLog:
    def __init__(self):
        self.logger = get_roblox_logger()

    def debug_script(self, script_name, msg):
        self.logger.debug(f'[{script_name}] {msg}')

    def error_api(self, code, msg):
        self.logger.error(f'API Failure {code}: {msg}')

logger = RobloxLog()