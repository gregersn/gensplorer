import os
import logging


def setup_logger(name, level="INFO"):
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    return logging.getLogger(name)