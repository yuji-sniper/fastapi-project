import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'sampleFormatter': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'sampleHandlers': {
            'class': 'logging.StreamHandler',
            'formatter': 'sampleFormatter',
            'level': logging.DEBUG
        }
    },
    'root': {
        'handlers': ['sampleHandlers'],
        'level': logging.WARNING,
    },
    'loggers': {
        'simpleExample': {
            'handlers': ['sampleHandlers'],
            'level': logging.DEBUG,
            'propagate': 0,
        }
    }
})

logger = logging.getLogger('simpleExample')

logger.warning('warning')
logger.error({
    'action': 'create',
    'status': 'fail',
    'message': 'Api call is failed.'
})
