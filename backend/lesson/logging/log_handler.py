import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('log_handler.log')
logger.addHandler(handler)


def do_something():
    logger.info('info')
    logger.debug('debug')
