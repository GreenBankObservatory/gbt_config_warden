"""Logging configuration for gbt_config_warden"""

import logging
import logging.config


def init_logging(log_dir=None):
    """Initialize logging. Write logs to given directory, or /tmp if not given"""
    if log_dir is None:
        log_dir = "/tmp"
    config = {
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
            },
            "file_debug": {
                "level": "DEBUG",
                "formatter": "verbose",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": f"{log_dir}/gbt_config_debug_log",
            },
            "file_std": {
                "level": "DEBUG",
                "formatter": "just_date",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": f"{log_dir}/gbt_config_change_log",
            },
        },
        "loggers": {
            "gbt_config_watch": {
                "handlers": ["console", "file_debug"],
                "level": "DEBUG",
            },
            "gbt_config_notify": {
                "handlers": ["console", "file_debug"],
                "level": "DEBUG",
            },
            "gbt_config_watch_file": {"handlers": ["file_std"], "level": "DEBUG",},
        },
    }
    logging.config.dictConfig(config)
