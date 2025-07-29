from functools import lru_cache
from logging import (
    Formatter,
    Handler,
    Logger,
    StreamHandler,
    getLogger,
)
from os import environ
from typing import Optional

__all__ = [
    "LoggerProvider",
]

ROOT_LOGGER_NAME = (
    environ.get("QENA_SHARED_LIB_LOGGING_LOGGER_NAME") or "qena_shared_lib"
)


class LoggerProvider:
    @lru_cache
    @staticmethod
    def default() -> "LoggerProvider":
        return LoggerProvider()

    @lru_cache
    def get_logger(self, name: str | None = None) -> Logger:
        logger_name = ROOT_LOGGER_NAME

        if name:
            logger_name = f"{ROOT_LOGGER_NAME}.{name.strip('.')}"

        logger = getLogger(logger_name)
        handlers = [handler.__class__ for handler in logger.handlers]

        if logger.parent is not None:
            self._check_handler(handlers=handlers, logger=logger.parent)

        if StreamHandler not in handlers:
            stream_handler = StreamHandler()

            stream_handler.setFormatter(
                Formatter(
                    "[ %(levelname)-8s] %(name)s [ %(filename)s:%(lineno)d in %(funcName)s ]  ---  %(message)s"
                )
            )
            logger.addHandler(stream_handler)

        return logger

    def _check_handler(
        self, handlers: list[type[Handler]], logger: Optional[Logger] = None
    ) -> None:
        if logger is None:
            return

        handlers.extend([handler.__class__ for handler in logger.handlers])
        self._check_handler(handlers=handlers, logger=logger.parent)
