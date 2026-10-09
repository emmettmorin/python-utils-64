import logging
from logging.handlers import RotatingFileHandler
import sys
import os

class RobloxLogger:
    def __init__(self, name='roblox_dev_bot', log_file='debug.log', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=1024 * 1024 * 5, 
                backupCount=3
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

def setup_roblox_logging(name='core', path='logs/session.log'):
    return RobloxLogger(name, path).get_logger()