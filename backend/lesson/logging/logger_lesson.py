import logging
import log_handler
import log_test


logging.basicConfig(level=logging.INFO)


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.debug('debug')

log_handler.do_something()
log_test.do_something()
