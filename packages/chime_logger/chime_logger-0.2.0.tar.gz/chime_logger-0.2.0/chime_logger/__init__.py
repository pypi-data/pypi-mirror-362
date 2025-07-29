import atexit
import logging
import logging.config
import queue
import sys
from logging.handlers import QueueHandler, QueueListener

from chime_logger.config import LOGGING_CONFIG


def setup_logging():
    """Configures logging for the CHIME logger package using the LOGGING_CONFIG dictionary.

    - Sets up handlers, formatters, and filters as specified in LOGGING_CONFIG.
    - Starts the QueueListener for the 'queue_handler' if it exists.
    - Registers atexit cleanup to stop the QueueListener on program exit.
    """
    if sys.version_info >= (3, 12):
        logging.config.dictConfig(LOGGING_CONFIG)
        queue_handler = logging.getHandlerByName("queue_handler")
    else:
        LOGGING_CONFIG["handlers"].pop("queue_handler")
        LOGGING_CONFIG["loggers"]["CHIME"]["handlers"] = ["loki"]
        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger("CHIME")
        queue_handler = QueueHandler(queue.Queue(-1))
        logger.addHandler(queue_handler)
        loki_handler = next(
            (h for h in logger.handlers if h.__class__.__name__ == "LokiHandler"),
            None,
        )
        logger.handlers.pop(0)
        listener = QueueListener(
            queue_handler.queue, loki_handler, respect_handler_level=True
        )
        queue_handler.listener = listener

    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
