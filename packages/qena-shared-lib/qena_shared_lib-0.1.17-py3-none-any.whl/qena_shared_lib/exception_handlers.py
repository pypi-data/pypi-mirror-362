from collections.abc import Iterable
from typing import Any, cast

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import to_jsonable_python

from .exceptions import (
    HTTPServiceError,
    RabbitMQServiceException,
    ServiceException,
    Severity,
)
from .logging import LoggerProvider
from .remotelogging import BaseRemoteLogSender

__all__ = [
    "AbstractHttpExceptionHandler",
    "GeneralHttpExceptionHandler",
    "HTTPServiceExceptionHandler",
    "RequestValidationErrorHandler",
]


class AbstractHttpExceptionHandler:
    @property
    def exception(self) -> type[Exception]:
        raise NotImplementedError()


class HTTPServiceExceptionHandler(AbstractHttpExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return cast(type[Exception], ServiceException)

    def __init__(
        self,
        remote_logger: BaseRemoteLogSender,
        logger_provider: LoggerProvider,
    ):
        self._remote_logger = remote_logger
        self._logger = logger_provider.get_logger("http.exception_handler")

    def __call__(
        self, request: Request, exception: ServiceException
    ) -> Response:
        exception_severity = exception.severity or Severity.LOW
        user_agent = request.headers.get("user-agent", "__unknown__")
        message = exception.message
        tags = [
            "HTTP",
            request.method,
            request.url.path,
            exception.__class__.__name__,
        ]
        extra = {
            "serviceType": "HTTP",
            "method": request.method,
            "path": request.url.path,
            "userAgent": user_agent,
            "exception": exception.__class__.__name__,
        }
        exc_info = (
            (type(exception), exception, exception.__traceback__)
            if exception.extract_exc_info
            else None
        )

        match exception_severity:
            case Severity.LOW:
                remote_logger_method = self._remote_logger.info
                logger_method = self._logger.info
            case Severity.MEDIUM:
                remote_logger_method = self._remote_logger.warning
                logger_method = self._logger.warning
            case _:
                message = "something went wrong"
                remote_logger_method = self._remote_logger.error
                logger_method = self._logger.error

        content: dict[str, Any] = {
            "severity": exception_severity.name,
            "message": message,
        }
        status_code = self._status_code_from_severity(exception.severity)
        headers = None

        match exception:
            case HTTPServiceError() as http_service_error:
                if http_service_error.body is not None:
                    extra_body = to_jsonable_python(http_service_error.body)
                    is_updated = False

                    try:
                        if isinstance(extra_body, Iterable):
                            content.update(extra_body)

                            is_updated = True
                    except:
                        pass

                    if not is_updated:
                        content["data"] = extra_body

                if http_service_error.response_code is not None:
                    content["code"] = http_service_error.response_code
                    str_response_code = str(http_service_error.response_code)
                    extra["responseCode"] = str_response_code

                    tags.append(str_response_code)

                if http_service_error.corrective_action is not None:
                    content["correctiveAction"] = (
                        http_service_error.corrective_action
                    )

                if http_service_error.status_code is not None:
                    status_code = http_service_error.status_code
                    str_status_code = str(status_code)
                    extra["statusCode"] = str_status_code

                    tags.append(str_status_code)

                if http_service_error.headers is not None:
                    headers = http_service_error.headers
            case RabbitMQServiceException() as rabbitmq_service_exception:
                str_error_code = str(rabbitmq_service_exception.code)
                extra["code"] = str_error_code

                tags.append(str_error_code)

        if exception.tags:
            tags.extend(exception.tags)

        if exception.extra:
            extra.update(exception.extra)

        if exception.remote_logging:
            remote_logger_method(
                message=exception.message,
                tags=tags,
                extra=extra,
                exception=exception if exception.extract_exc_info else None,
            )
        else:
            logger_method(
                "\n%s %s\n%s",
                request.method,
                request.url.path,
                exception.message,
                exc_info=exc_info,
            )

        return JSONResponse(
            content=content,
            status_code=status_code,
            headers=headers,
        )

    def _status_code_from_severity(self, severity: Severity | None) -> int:
        if (
            severity is None
            or severity is Severity.LOW
            or severity is Severity.MEDIUM
        ):
            return cast(int, status.HTTP_400_BAD_REQUEST)

        return cast(int, status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestValidationErrorHandler(AbstractHttpExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return cast(type[Exception], RequestValidationError)

    def __init__(self, logger_provider: LoggerProvider):
        self._logger = logger_provider.get_logger("http.exception_handler")

    def __call__(
        self, request: Request, error: RequestValidationError
    ) -> Response:
        message = "invalid request data"

        self._logger.warning(
            "\n%s %s\n%s", request.method, request.url.path, message
        )

        return JSONResponse(
            content={
                "severity": Severity.MEDIUM.name,
                "message": message,
                "code": 100,
                "detail": to_jsonable_python(error.errors()),
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


class GeneralHttpExceptionHandler(AbstractHttpExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return Exception

    def __init__(self, remote_logger: BaseRemoteLogSender):
        self._remote_logger = remote_logger

    def __call__(self, request: Request, exception: Exception) -> Response:
        user_agent = request.get("user-agent", "__unknown__")

        self._remote_logger.error(
            message=f"something went wrong on endpoint `{request.method} {request.url.path}`",
            tags=[
                "HTTP",
                request.method,
                request.url.path,
                exception.__class__.__name__,
            ],
            extra={
                "serviceType": "HTTP",
                "method": request.method,
                "path": request.url.path,
                "userAgent": user_agent,
                "exception": exception.__class__.__name__,
            },
            exception=exception,
        )

        return JSONResponse(
            content={
                "severity": Severity.HIGH.name,
                "message": "something went wrong",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
