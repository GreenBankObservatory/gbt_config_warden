import logging
import logging.config
import os

CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s",
        },
        "just_date": {"format": "%(asctime)s: %(message)s",},
        "super_simple": {"format": "%(message)s",},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            # Log to console only in debug mode
            # 'filters': ['filters.OnlyInDebugFilter']
        },
        "file_debug": {
            "level": "DEBUG",
            "formatter": "verbose",
            "class": "logging.handlers.WatchedFileHandler",
            # 'class': 'handlers.DatestampFileHandler',
            "filename": "/tmp/foo",
        },
        "file_std": {
            "level": "DEBUG",
            "formatter": "just_date",
            "class": "logging.handlers.WatchedFileHandler",
            # 'class': 'handlers.DatestampFileHandler',
            "filename": "/tmp/gbt_config_change_log",
        },
    },
    "loggers": {
        # 'root': {'level': 'DEBUG'},
        "cwp": {
            "handlers": ["console", "file_debug"],
            # Make sure we don't miss anything...
            "level": "DEBUG",
        },
        "cwp_file": {
            "handlers": ["file_std"],
            "level": "DEBUG",
        }
    },
    # "root": {"level": "DEBUG", "handlers": ["console"]},
}


def init_logging(log_path):
    # CONFIG['handlers']['file']['filename'] = log_path
    logging.config.dictConfig(CONFIG)
