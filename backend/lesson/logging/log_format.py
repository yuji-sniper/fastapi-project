import logging

formatter = '%(asctime)s:%(levelname)s:%(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

logging.error('error')
logging.info('info')
