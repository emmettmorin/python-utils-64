import logging
import os
from logging.handlers import RotatingFileHandler

def get_roblox_logger(name='rbx_logger', log_file='rbx_ops.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        rotating_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

def rotate_forcefully(logger):
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler):
            handler.doRollover()
            
if __name__ == '__main__':
    log = get_roblox_logger()
    log.info('System initialized for Roblox automation tasks')