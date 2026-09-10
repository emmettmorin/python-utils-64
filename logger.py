import logging
import os
from logging.handlers import RotatingFileHandler

def setup_roblox_logger(name: str = "roblox_bot", log_dir: str = "logs") -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_path = os.path.join(log_dir, f"{name}.log")
    file_handler = RotatingFileHandler(
        file_path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

log = setup_roblox_logger()