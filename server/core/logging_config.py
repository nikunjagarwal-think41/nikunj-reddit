import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create a logger
    logger = logging.getLogger("goss_app")
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = RotatingFileHandler("app.log", maxBytes=1024*1024*5, backupCount=2)
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
