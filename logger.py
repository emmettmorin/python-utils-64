import logging
import os
from logging.handlers import RotatingFileHandler

def get_roblox_logger(name='rbx-utils', log_dir='logs'):
    """ Initialize logger with size-based rotation for Roblox scripts """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    path = os.path.join(log_dir, f"{name}.log")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = RotatingFileHandler(
            path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

# Quick access instance
rbx_logger = get_roblox_logger()