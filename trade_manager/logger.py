import logging

def setup_logger():
    logging.basicConfig(filename='bot.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message, level=logging.INFO):
    """Log a message with the specified level."""
    if level == logging.DEBUG:
        logging.debug(message)
    elif level == logging.INFO:
        logging.info(message)
    elif level == logging.WARNING:
        logging.warning(message)
    elif level == logging.ERROR:
        logging.error(message)
    elif level == logging.CRITICAL:
        logging.critical(message)
    else:
        logging.info(message)
