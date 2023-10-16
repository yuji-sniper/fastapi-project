import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def do_something():
    logger.info('from log_test info')
    logger.debug('from log_test debug')
