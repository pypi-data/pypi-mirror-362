import logging
from pythonjsonlogger import jsonlogger

def initLog(name, leve=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # log_formatter = logging.Formatter("%(filename)s %(funcName)s %(lineno)s %(asctime)s %(levelname)s %(name)s %(message)s")
    log_formatter = jsonlogger.JsonFormatter('%(filename)s %(funcName)s %(lineno)s %(asctime)s %(levelname)s %(name)s %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger