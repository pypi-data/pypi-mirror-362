"""Configuration for the CHIME logging system."""

import os
import pathlib

DEFAULT_LOKI_URL = "https://frb.chimenet.ca/loki/loki/api/v1/push"
DEFAULT_LOKI_TENANT = "CHIME"
DEFAULT_FILE_LOG_PATH = "logs/my_app.logs"

LOKI_AUTH = (
    (
        os.getenv("CHIME_LOGGER_LOKI_USER"),
        os.getenv("CHIME_LOGGER_LOKI_PASSWORD"),
    )
    if os.getenv("CHIME_LOGGER_LOKI_USER") and os.getenv("CHIME_LOGGER_LOKI_PASSWORD")
    else None
)


def check_file_log_path_valid(path: str) -> str:
    """Check if the file log path is valid and return the absolute path.

    Args:
        path (str): The file log path to check.

    Returns:
        str: The absolute path of the file log.
    """
    abs_path = pathlib.Path(path).expanduser().resolve()
    if not abs_path.parent.exists():
        abs_path.parent.mkdir(parents=True, exist_ok=True)
    return str(abs_path)


# TODO: Allow pushing to multiple Loki instances
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[ pipeline=%(pipeline)s event=%(event)s ] %(message)s"},
        "detailed": {
            "format": "%(asctime)s [ pipeline=%(pipeline)s event=%(event)s ] %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "filters": {
        "add_pipeline_filter": {"()": "chime_logger.filters.PipelineFilter"},
        "add_event_filter": {"()": "chime_logger.filters.EventFilter"},
    },
    "handlers": {
        "loki": {
            "()": "chime_logger.handlers.LokiHandler",
            "level": "INFO",
            "formatter": "simple",
            "filters": ["add_pipeline_filter", "add_event_filter"],
            "url": os.getenv("CHIME_LOGGER_LOKI_URL", DEFAULT_LOKI_URL),
            "auth": LOKI_AUTH,
            "headers": {
                "X-Scope-OrgID": os.getenv(
                    "CHIME_LOGGER_LOKI_TENANT", DEFAULT_LOKI_TENANT
                )
            },
            "version": "2",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            # BUG: This can fail if the directory does not exist
            "filename": check_file_log_path_valid(
                os.getenv("CHIME_LOGGER_FILE_LOG_PATH", DEFAULT_FILE_LOG_PATH)
            ),
            "maxBytes": 10_000_000,
            "backupCount": 3,
        },
        "queue_handler": {
            "class": "logging.handlers.QueueHandler",
            "handlers": ["loki", "file"],
            "filters": ["add_pipeline_filter", "add_event_filter"],
            "respect_handler_level": True,
        },
    },
    "loggers": {
        "CHIME": {"level": "INFO", "handlers": ["queue_handler"], "propagate": False}
    },
}
