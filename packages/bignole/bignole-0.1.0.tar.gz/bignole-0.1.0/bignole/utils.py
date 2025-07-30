# -*- coding: utf-8 -*-


import copy
import logging
import logging.config
import logging.handlers
import sys


LOG_NAMESPACE = "bignole"


def get_syslog_address():  # pylint: disable-msg=missing-function-docstring
    if sys.platform.startswith("linux"):
        return "/dev/log"
    if sys.platform == "darwin":
        return "/var/run/syslog"
    return "localhost", logging.handlers.SYSLOG_UDP_PORT


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "debug": {"format": "[%(levelname)s] %(name)30s:%(lineno)d %(message)s"},
        "simple": {"format": "%(message)s"},
        "verbose": {"format": "[%(levelname)s] %(message)s"},
        "syslog": {"format": f"{LOG_NAMESPACE}[%(process)d]: %(message)s"},
    },
    "handlers": {
        "stderr": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "syslog": {
            "level": "ERROR",
            "class": "logging.handlers.SysLogHandler",
            "formatter": "syslog",
            "address": get_syslog_address(),
        },
    },
    "loggers": {
        LOG_NAMESPACE: {"handlers": ["syslog"], "level": "DEBUG", "propagate": True}
    },
}


def topen(filename, write=False):
    """Open a file with errors='surrogateescape'"""
    mode = "w" if write else "r"
    return open(filename, mode, encoding="utf-8", errors="surrogateescape")


def get_content(filename):
    """Read all the content of a file"""
    with topen(filename) as filefp:
        return filefp.read()


def logger(namespace):  # pylint: disable-msg=missing-function-docstring
    return logging.getLogger(f"{LOG_NAMESPACE}.{namespace}")


def configure_logging(debug=False, verbose=True, stderr=True):  # pylint: disable-msg=missing-function-docstring
    config = copy.deepcopy(LOG_CONFIG)

    for handler in config["handlers"].values():
        if verbose:
            handler["level"] = "INFO"
        if debug:
            handler["level"] = "DEBUG"

    if verbose:
        config["handlers"]["stderr"]["formatter"] = "verbose"
    if debug:
        config["handlers"]["stderr"]["formatter"] = "debug"

    if stderr:
        config["loggers"][LOG_NAMESPACE]["handlers"].append("stderr")

    logging.config.dictConfig(config)
