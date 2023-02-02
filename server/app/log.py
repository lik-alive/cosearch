import logging

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 10000,
            'backupCount': 10
        },
        'info': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/info.log',
            'maxBytes': 10000,
            'backupCount': 10
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['default']
        },
        'info': {
            'level': 'DEBUG',
            'handlers': ['info'],
            'propagate': False
        }
    },
}


class log:
    """Init logger"""
    @staticmethod
    def init():
        logging.config.dictConfig(LOGGING_CONFIG)

    """Write info log"""
    @staticmethod
    def info(msg):
        info = logging.getLogger('info')
        info.info(msg)

    """Write error log"""
    @staticmethod
    def error(msg):
        logging.error(msg)
