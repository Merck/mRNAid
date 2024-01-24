from loguru import logger
import os


def MyLogger(name):
    """ Logger which can be imported to any module """

    logger.remove()

    logger.level("DEBUG", color="<yellow>")
    logger.level("INFO", color="<green>")
    logger.level("ERROR", color="<red>")

    file = os.environ.get('LOG_FILE')

    if file:
        log_format = "{time:YYYY-MMMM-DD,dddd    HH:mm:ss:A}| {module}| {level}| {message}"
        logger.add(file, format=log_format, level="DEBUG", backtrace=True, rotation="100 MB", compression="zip",
                   enqueue=True)
    logger.enable(name)

    return logger
