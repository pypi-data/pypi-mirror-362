# -*- coding: utf-8 -*-

"""
Logger for handling sound/voice/audio data.
"""

import logging

LOG_FMT = "[%(asctime)s.%(msecs)03d][%(levelname)s][%(module)s][%(funcName)s,%(lineno)s]: %(message)s"
LOG_LEVEL = logging.INFO
LOGGER_NAME = "seasalt.speech"


def get_logger() -> logging.Logger:
    formatter = logging.Formatter(LOG_FMT, "%Y-%m-%dT%H:%M:%S")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(LOG_LEVEL)

    logger = logging.getLogger(name=LOGGER_NAME)
    logger.propagate = False
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(stream_handler)
    return logger


default_logger = get_logger()
