import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


class KSTFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt="%Y-%m-%d %H:%M:%S", style="%"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.datefmt = datefmt

    def formatTime(self, record, datefmt=None):
        kst_time = datetime.fromtimestamp(record.created, tz=KST)
        if datefmt:
            s = kst_time.strftime(datefmt)
        else:
            s = kst_time.strftime(self.datefmt)
        return s

    def format(self, record):
        log_message = super().format(record)
        divide = "-" * 100
        return f"\n{divide}\n\n{log_message}"


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG
LOG_FILE = "app.log"

formatter = KSTFormatter(LOG_FORMAT)

file_handler = RotatingFileHandler(LOG_FILE)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)


def log_exception(exception: Exception):
    exc_info = (type(exception), exception, exception.__traceback__)
    logger.error("Exception occurred.", exc_info=exc_info)
