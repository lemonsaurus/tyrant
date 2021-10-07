import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    A handler to push standard logging messages to loguru.

    This is directly from the loguru docs.
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Push all std lib logger calls to loguru
logging.basicConfig(handlers=[InterceptHandler()], level=0)

# Silence noisy libs
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

# Remove the default stderr sink, so we can add our own with custom formatting.
logger.remove()

# Define logger format and add the sink.
logger_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name}:{line} | {message}"
logger.add(sys.stdout, format=logger_format)
