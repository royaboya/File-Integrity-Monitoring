import logging
from logging.handlers import RotatingFileHandler
import os

# change params
def initialize_logger(p1, p2, max_bytes):
        
    logging_inst = logging.getLogger(__name__)
    logging_inst.setLevel(logging.DEBUG)
     
    setup_handlers(logging_inst, p1, p2, max_bytes)
     
    return logging_inst

def setup_handlers(logger, info_log_path, error_log_path, max_bytes=5_000_000):
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    info_handler = RotatingFileHandler(info_log_path, maxBytes=max_bytes, backupCount=2)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(os.path.join(error_log_path), maxBytes=max_bytes, backupCount=2)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    
logger = logging.getLogger(__name__)

