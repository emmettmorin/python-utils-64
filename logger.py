import logging
import os
from logging.handlers import RotatingFileHandler

def get_roblox_logger(name='roblox_dev_logger', log_file='debug.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(name)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=2*1024*1024, 
            backupCount=5,
            encoding='utf-8'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate singleton for global usage across modules
roblox_logger = get_roblox_logger()