import logging
from logging.handlers import RotatingFileHandler
import os

def get_roblox_logger(name='rbx-logger', log_file='session.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] (roblox-engine) -> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    file_path = os.path.join('logs', log_file)
    rotate_handler = RotatingFileHandler(
        file_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    rotate_handler.setFormatter(formatter)
    logger.addHandler(rotate_handler)
    
    return logger

rbx_log = get_roblox_logger()