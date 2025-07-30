import json
import logging


class JsonFormatter(logging.Formatter):
    """
    Custom formatter to convert a log record's message (a dict) into a JSON string.
    """

    def format(self, record):
        # The 'extra' dictionary passed to the logger becomes part of the record's __dict__
        # We ensure that the core message is a dictionary that gets dumped to JSON
        if isinstance(record.msg, dict):
            return json.dumps(record.msg)
        return super().format(record)


def setup_json_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger that writes records as JSON lines to a file.
    """
    # Ensure logs aren't duplicated by upstream loggers
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False  # Prevent the log from being passed to the root logger

    return logger
