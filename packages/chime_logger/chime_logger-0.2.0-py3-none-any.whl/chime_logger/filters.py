"""This module provides custom logging filters for the CHIME logger.

Classes:
    PipelineFilter: Ensures log records have a 'pipeline' attribute.
    EventFilter: Ensures log records have an 'event' attribute.
"""

import logging
import os


class PipelineFilter(logging.Filter):
    """Logging filter that ensures each log record has a 'pipeline' attribute.

    If the 'pipeline' attribute is missing, it sets it to the value of the
    'CHIME_LOGGER_PIPELINE_NAME' environment variable, or 'unknown_pipeline'
    if the environment variable is not set.
    """

    def filter(self, record):
        """Ensures that each log record has a 'pipeline' attribute.

        If the 'pipeline' attribute is missing from the log record, this method sets it
        to the value of the 'CHIME_LOGGER_PIPELINE_NAME' environment variable, or
        'unknown_pipeline' if the environment variable is not set.

        Args:
            record (logging.LogRecord): The log record to filter.

        Returns:
            bool: Always returns True to allow the record to be processed.
        """
        # If the record does not have a 'pipeline' attribute, set it to a default value
        if not hasattr(record, "pipeline"):
            record.pipeline = os.getenv(
                "CHIME_LOGGER_PIPELINE_NAME", "unknown_pipeline"
            )
        return True


class EventFilter(logging.Filter):
    """Logging filter that ensures each log record has an 'event' attribute.

    If the 'event' attribute is missing, it sets it to 'unknown_event'.
    """

    def filter(self, record):
        """Ensures that each log record has an 'event' attribute.

        If the 'event' attribute is missing from the log record, this method sets it
        to 'unknown_event'.

        Args:
            record (logging.LogRecord): The log record to filter.

        Returns:
            bool: Always returns True to allow the record to be processed.
        """
        # If the record does not have an 'event' attribute, set it to a default value
        if not hasattr(record, "event"):
            record.event = "unknown_event"
        return True
