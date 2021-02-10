import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standart': {
            'format': '%(asctime)s - %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': 'log.txt',
            'mode': 'a',
            'maxBytes': 10240,
            'backupCount': 0,
            'formatter': 'standart',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['file_handler'],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('root')
