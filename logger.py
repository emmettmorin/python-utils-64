import logging
from logging.handlers import RotatingFileHandler
import os

def get_roblox_logger(name='roblox_dev', log_file='debug.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

class RobloxLogAdapter:
    """Injects context into roblox-dev logs"""
    def __init__(self, logger, context):
        self.logger = logger
        self.context = context

    def info(self, msg):
        self.logger.info(f"[{self.context}] {msg}")

    def error(self, msg):
        self.logger.error(f"[{self.context}] {msg}")