import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class RobloxLogger:
    def __init__(self, name='roblox_dev', log_dir='logs'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        log_path = os.path.join(log_dir, f'{name}.log')
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=1024 * 1024 * 5,
            backupCount=3
        )
        
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

def setup_roblox_logging(name='roblox_dev'):
    return RobloxLogger(name).get_logger()