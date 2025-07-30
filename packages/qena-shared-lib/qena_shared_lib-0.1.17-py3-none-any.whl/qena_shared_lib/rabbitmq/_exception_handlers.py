from typing import cast

from pydantic import ValidationError

from ..exceptions import (
    HTTPServiceError,
    RabbitMQServiceException,
    ServiceException,
    Severity,
)
from ..logging import LoggerProvider
from ..remotelogging._base import BaseRemoteLogSender
from ._listener import ListenerContext

__all__ = [
    "AbstractRabbitMqExceptionHandler",
    "GeneralMqExceptionHandler",
    "RabbitMqServiceExceptionHandler",
    "ValidationErrorHandler",
]

RABBITMQ_EXCEPTION_HANDLER_LOGGER_NAME = "rabbitmq.exception_handler"


class AbstractRabbitMqExceptionHandler:
    @property
    def exception(self) -> type[Exception]:
        raise NotImplementedError()


class RabbitMqServiceExceptionHandler(AbstractRabbitMqExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return cast(type[Exception], ServiceException)

    def __init__(
        self,
        remote_logger: BaseRemoteLogSender,
        logger_provider: LoggerProvider,
    ):
        self._logger = logger_provider.get_logger(
            RABBITMQ_EXCEPTION_HANDLER_LOGGER_NAME
        )
        self._remote_logger = remote_logger

    def __call__(
        self,
        context: ListenerContext,
        exception: ServiceException,
    ) -> None:
        tags = [
            "RabbitMQ",
            context.queue,
            context.listener_name or "__default__",
            exception.__class__.__name__,
        ]
        extra = {
            "serviceType": "RabbitMQ",
            "queue": context.queue,
            "listenerName": context.listener_name,
            "exception": exception.__class__.__name__,
        }

        match exception:
            case HTTPServiceError() as http_service_error:
                if http_service_error.status_code is not None:
                    str_status_code = str(http_service_error.status_code)
                    extra["statusCode"] = str_status_code

                    tags.append(str_status_code)

                if http_service_error.response_code is not None:
                    str_response_code = str(http_service_error.response_code)
                    extra["responseCode"] = str_response_code

                    tags.append(str_response_code)
            case RabbitMQServiceException() as rabbitmq_service_exception:
                str_error_code = str(rabbitmq_service_exception.code)
                extra["code"] = str_error_code

                tags.append(str_error_code)

        if exception.tags:
            tags.extend(exception.tags)

        if exception.extra:
            extra.update(exception.extra)

        exc_info = (
            (type(exception), exception, exception.__traceback__)
            if exception.extract_exc_info
            else None
        )

        match exception.severity:
            case Severity.HIGH:
                remote_logger_method = self._remote_logger.error
                logger_method = self._logger.error
            case Severity.MEDIUM:
                remote_logger_method = self._remote_logger.warning
                logger_method = self._logger.warning
            case _:
                remote_logger_method = self._remote_logger.info
                logger_method = self._logger.info

        if exception.remote_logging:
            remote_logger_method(
                message=exception.message,
                tags=tags,
                extra=extra,
                exception=exception if exception.extract_exc_info else None,
            )
        else:
            logger_method(
                "\nRabbitMQ `%s` -> `%s`\n%s",
                context.queue,
                context.listener_name,
                exception.message,
                exc_info=exc_info,
            )


class ValidationErrorHandler(AbstractRabbitMqExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return cast(type[Exception], ValidationError)

    def __init__(self, remote_logger: BaseRemoteLogSender):
        self._remote_logger = remote_logger

    def __call__(
        self,
        context: ListenerContext,
        exception: ValidationError,
    ) -> None:
        self._remote_logger.error(
            message=f"invalid rabbitmq request data at queue `{context.queue}` and listener `{context.listener_name}`",
            tags=[
                "RabbitMQ",
                context.queue,
                context.listener_name or "__default__",
                "ValidationError",
            ],
            extra={
                "serviceType": "RabbitMQ",
                "queue": context.queue,
                "listenerName": context.listener_name,
                "exception": "ValidationError",
            },
            exception=exception,
        )


class GeneralMqExceptionHandler(AbstractRabbitMqExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return Exception

    def __init__(self, remote_logger: BaseRemoteLogSender):
        self._remote_logger = remote_logger

    def __call__(
        self,
        context: ListenerContext,
        exception: Exception,
    ) -> None:
        self._remote_logger.error(
            message=f"something went wrong while consuming message on queue `{context.queue}` and listener `{context.listener_name}`",
            tags=[
                "RabbitMQ",
                context.queue,
                context.listener_name or "__default__",
                exception.__class__.__name__,
            ],
            extra={
                "serviceType": "RabbitMQ",
                "queue": context.queue,
                "listenerName": context.listener_name,
                "exception": exception.__class__.__name__,
            },
            exception=exception,
        )
