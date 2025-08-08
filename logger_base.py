import logging
from colorlog import ColoredFormatter

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        log_format = '%(log_color)s%(name)s - %(levelname)s - %(message)s'
        formatter = ColoredFormatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
