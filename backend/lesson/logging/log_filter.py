import logging
from logging import LogRecord


logging.basicConfig(level=logging.INFO)


class NoPassFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        log_message = record.getMessage()
        return 'password' not in log_message


logger = logging.getLogger(__name__)
logger.addFilter(NoPassFilter())
logger.info('info')
logger.info('info password = xxxx')
