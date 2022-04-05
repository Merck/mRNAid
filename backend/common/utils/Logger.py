from loguru import logger
import os


def MyLogger(name):
    """ Logger which can be imported to any module """

    print(f'Logger passed name {name}')
    logger.remove()

    logger.level("DEBUG", color="<yellow>")
    logger.level("INFO", color="<green>")
    logger.level("ERROR", color="<red>")

    file = os.environ['LOG_FILE']
    log_format = "{time:YYYY-MMMM-DD,dddd    HH:mm:ss:A}| {module}| {level}| {message}"

    logger.add(file, format=log_format, level="DEBUG", backtrace=True, rotation="100 MB", compression="zip",
               enqueue=True)
    logger.enable(name)

    return logger
