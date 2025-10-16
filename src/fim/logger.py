import logging

def initialize_logger(filename, text_encoding, level):
        
    logging.basicConfig(
        filename=filename,
        encoding=text_encoding,
        level=level
    )
   
    logging_inst = logging.getLogger(__name__)
     
    return logging_inst


# need to add handler and set format

logger = logging.getLogger(__name__)

