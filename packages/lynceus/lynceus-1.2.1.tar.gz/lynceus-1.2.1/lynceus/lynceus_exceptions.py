from lynceus.utils import format_exception_human_readable


class LynceusError(Exception):
    """Base Lynceus exception, all specific exceptions inherits from it."""

    def __init__(self, message, from_exception: Exception | None = None):
        super().__init__()
        self.__message = message
        if from_exception:
            self.__message += f'; caused by {format_exception_human_readable(from_exception, quote_message=True)}.'

    def __str__(self):
        return self.__message


class LynceusConfigError(LynceusError):
    pass


class LynceusJobError(LynceusError):
    pass


class LynceusJobCancelExecutionError(LynceusJobError):
    pass


class LynceusFileError(LynceusError):
    pass
