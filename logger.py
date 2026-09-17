import logging
from logging.handlers import RotatingFileHandler
import os

def setup_roblox_logger(name: str = "roblox_proc", log_file: str = "roblox.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s | [%(levelname)s] | %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

log = setup_roblox_logger()

def log_event(msg: str, level: str = "info"):
    """Dynamic dispatch for roblox event tracing."""
    methods = {
        "info": log.info,
        "warn": log.warning,
        "error": log.error,
        "debug": log.debug
    }
    func = methods.get(level, log.info)
    func(f"[RPC-SYNC] {msg}")