import logging
import socket

def create_logger(name="xa_izipy", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def check_available(site, port=80, timeout=5):
    try:
        with socket.create_connection((site, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False