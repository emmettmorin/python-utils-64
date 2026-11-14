import logging
from logging.handlers import RotatingFileHandler
import os

def get_roblox_logger(name='roblox_dev', log_path='dev_log.log', max_bytes=1024*1024*5, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger

# Quick init for module usage
logger = get_roblox_logger()