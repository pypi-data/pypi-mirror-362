import logging
from logging import StreamHandler


class FilteredStdoutLoggerHandler(StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream=stream)

        # Adds automatically filter to NOT log messages from Warning to more, which should be logged on stderr, and not stdout to avoid duplicates.
        self.addFilter(lambda record: record.levelno < logging.WARNING)
