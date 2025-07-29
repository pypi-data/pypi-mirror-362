import logging
import time
from abc import ABCMeta
from datetime import datetime, timezone
from logging import CRITICAL, DEBUG, ERROR, INFO, Logger, WARNING

from .config import CONFIG_LOG_MESSAGE_STATUS_KEY
from .exchange.lynceus_exchange import LynceusExchange
from .lynceus import LynceusSession
from .lynceus_message_status import LynceusMessageStatus


class LynceusClientLogExchangeWrapper(Logger):
    # Defines a threshold for automatic message status definition (can be: 0, WARNING, or ERROR).
    AUTOMATIC_MESSAGE_STATUS_LOG_LEVEL_THRESHOLD: int = ERROR

    # N.B.: Logger has already been initialized, and specified as argument, so we do NOT want to call super __init__ method.
    # pylint: disable=super-init-not-called
    def __init__(self, logger: Logger, lynceus_exchange: LynceusExchange | None):
        self.__logger: Logger = logger
        self._lynceus_exchange: LynceusExchange | None = lynceus_exchange

    # Adds various properties wrapping around internal logger property allowing to use custom Level like TRACE.
    @property
    def name(self) -> str:
        return self.__logger.name

    @property
    def level(self) -> int:
        return self.__logger.level

    @property
    def parent(self):
        return self.__logger.parent

    @property
    def propagate(self) -> bool:
        return self.__logger.propagate

    @property
    def handlers(self) -> list[logging.Handler]:
        return self.__logger.handlers

    @property
    def filters(self):
        return self.__logger.filters

    @property
    def disabled(self) -> bool:
        return self.__logger.disabled

    @property
    def root(self):
        return self.__logger.root

    @property
    def manager(self) -> logging.Manager:
        return self.__logger.manager

    @property
    def _cache(self):
        # pylint: disable=protected-access
        return self.__logger._cache

    def __manage_logging(self, log_level: int, msg, *args, **kwargs):
        message_status: LynceusMessageStatus | None = kwargs.pop(CONFIG_LOG_MESSAGE_STATUS_KEY, None)

        # Defines automatically message status for warning and error.
        if not message_status \
                and log_level >= LynceusClientLogExchangeWrapper.AUTOMATIC_MESSAGE_STATUS_LOG_LEVEL_THRESHOLD:
            message_status = LynceusMessageStatus.ERROR if log_level == ERROR else LynceusMessageStatus.WARNING

        if self._lynceus_exchange:
            # Creates an **object** somehow like Log Record, which will be consumed by caller (like API).
            # queue_message: LogRecord = self.__logger.makeRecord(self.__logger.name, log_level, None, None, msg, args, exc_info=None, func=None, extra=None, sinfo=None)
            queue_message = {
                'asctime': datetime.now(tz=timezone.utc).strftime('%Y/%m/%d %H:%M:%S'),
                'created': time.time(),
                'levelname': logging.getLevelName(log_level),
                'name': self.__logger.name,
                'message': msg,
                'message_status': message_status
            }

            # Puts the message in Lynceus exchange.
            self._lynceus_exchange.put_nowait(queue_message)

        # Requests true logging anyway.
        if message_status:
            msg += f' [{CONFIG_LOG_MESSAGE_STATUS_KEY}={message_status}]'

        self.__logger.log(log_level, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(LynceusSession.TRACE, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        # Intercepts the call, to registers message in the lynceus exchange.
        self.__manage_logging(CRITICAL, msg, *args, **kwargs)


class LynceusClientClass(metaclass=ABCMeta):
    def __init__(self, lynceus_session: LynceusSession, logger_name: str, lynceus_exchange: LynceusExchange | None):
        self._lynceus_session: LynceusSession = lynceus_session
        self._lynceus_exchange = lynceus_exchange
        self.__logger: Logger = self._lynceus_session.get_logger(logger_name)

        # Declares the self._logger attribute with Lynceus wrapper (with/out lynceus_exchange).
        self._logger: LynceusClientLogExchangeWrapper = LynceusClientLogExchangeWrapper(self.__logger, self._lynceus_exchange)
