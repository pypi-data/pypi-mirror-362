import logging


class ConsoleLogsFormatter(logging.Formatter):
    grey = "\x1b[0;37;1m"
    yellow = "\x1b[1;33;20m"
    blue = "\x1b[0;34;20m"
    highlight_red = "\x1b[0;30;41m"
    bold_red = "\x1b[1;31;1m"
    red = "\x1b[0;31;20m"
    green="\x1b[0;32;20m"
    reset = "\x1b[0m"
    # format = LOGGER_CONFIG.LOG_FORMAT
    date_format = "%%Y-%%m-%%d %%H:%%M:%%S"

    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: highlight_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.date_format)
        return formatter.format(record)


# Set up the logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
cf = ConsoleLogsFormatter()
handler.setFormatter(cf)
# Set the formatter to the handler
# handler.setFormatter(cf)

# Add the handler to the logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # Set the level to DEBUG or any other level you prefer

# logging.basicConfig(level=logging.INFO,, format='%(asctime)s - %(levelname)s - %(message)s')

# logger = logging.getLogger(__name__)


