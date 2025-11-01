import logging

def initialize_logger(filename, text_encoding, level, format):
        
    logging.basicConfig(
        filename=filename,
        encoding=text_encoding,
        level=level,
        format=format
    )
   
    logging_inst = logging.getLogger(__name__)
     
    return logging_inst

logger = logging.getLogger(__name__)

