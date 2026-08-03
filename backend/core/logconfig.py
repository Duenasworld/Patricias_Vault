import logging.config

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s: %(levelname)s: %(user)s - %(message)s',
            'datefmt': '%d.%m.%Y %H:%M:%S'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'slwbpyui': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

def do_config():
    logging.config.dictConfig(DEFAULT_LOGGING)