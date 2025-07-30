from asyncio import get_running_loop
from base64 import b64decode
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from socketserver import StreamRequestHandler, TCPServer
from threading import Thread
from typing import Any, Callable, Generator

from pytest import fixture, mark, raises
from typing_extensions import Self

from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    LogLevel,
    RemoteLogRecord,
    SenderResponse,
)
from qena_shared_lib.remotelogging.logstash import (
    BaseLogstashSender,
    HTTPSender,
    TCPSender,
)
from tests.utils import random_port

http_logs: list[dict[str, Any]] = []
tcp_logs: list[dict[str, Any]] = []


class LogstashHttpServer(BaseHTTPRequestHandler):
    def do_post(self) -> None:
        content_length = self.headers.get("content-length")
        authorization = self.headers.get("authorization")

        if content_length is None:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.end_headers()
            self.wfile.write(b"bad request")

            return

        if authorization is not None:
            if not authorization.startswith("Basic "):
                self.send_response(HTTPStatus.UNAUTHORIZED)
                self.end_headers()
                self.wfile.write(b"unauthorized")

                return

            user, password, *_ = (
                b64decode(authorization.lstrip("Basic ")).decode().split(":")
            )

            if user != "user" or password != "password":
                self.send_response(HTTPStatus.UNAUTHORIZED)
                self.end_headers()
                self.wfile.write(b"unauthorized")

                return

        try:
            http_logs.append(loads(self.rfile.read(int(content_length))))
        except Exception:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()
            self.wfile.write(b"internal server error")
        else:
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b"ok")

    @classmethod
    def with_method_alias(cls) -> type[Self]:
        setattr(cls, "do_POST", cls.do_post)

        return cls


class LogstashTcpServer(StreamRequestHandler):
    def handle(self) -> None:
        while not self.rfile.closed:
            try:
                log = self.rfile.readline()

                if log == b"":
                    return

                tcp_logs.append(loads(log))
            except Exception:
                pass


@fixture(scope="module", autouse=True)
def logstash_http_server() -> Generator[int, None, None]:
    logstash_port = random_port()
    logstash_server = HTTPServer(
        ("0.0.0.0", logstash_port), LogstashHttpServer.with_method_alias()
    )
    logstash_server_thread = Thread(target=logstash_server.serve_forever)

    logstash_server_thread.start()

    yield logstash_port

    logstash_server.shutdown()
    logstash_server_thread.join()


@fixture(scope="module", autouse=True)
def logstash_tcp_server() -> Generator[int, None, None]:
    logstash_port = random_port()
    logstash_server = TCPServer(("0.0.0.0", logstash_port), LogstashTcpServer)
    logstash_server_thread = Thread(target=logstash_server.serve_forever)

    logstash_server_thread.start()

    yield logstash_port

    logstash_server.shutdown()
    logstash_server_thread.join()


@mark.asyncio
async def test_logstash_http_sender(logstash_http_server: int) -> None:
    logstash = HTTPSender(
        url=f"http://127.0.0.1:{logstash_http_server}",
        service_name="test",
        http_client_timeout=120,
    )

    logstash.set_level(LogLevel.DEBUG)

    await logstash.start()

    logstash.log(LogLevel.DEBUG, "tpc log message")
    logstash.debug("http debug message")
    logstash.info("http info message")
    logstash.warning("http warning message")
    logstash.error("http error message")

    await logstash.stop()

    assert len(http_logs) == 5


@mark.asyncio
async def test_logstash_http_sender_auth(logstash_http_server: int) -> None:
    http_logs.clear()

    logstash = HTTPSender(
        url=f"http://127.0.0.1:{logstash_http_server}",
        user="user",
        password="password",
        service_name="test",
        http_client_timeout=120,
    )

    await logstash.start()

    logstash.info("http info message")

    await logstash.stop()

    assert len(http_logs) == 1


@mark.asyncio
async def test_logstash_http_sender_wrong_auth(
    logstash_http_server: int,
) -> None:
    http_logs.clear()

    logstash = HTTPSender(
        url=f"http://127.0.0.1:{logstash_http_server}",
        user="wrong_user",
        password="wrong_password",
        service_name="test",
        max_log_retry=0,
        http_client_timeout=120,
    )

    await logstash.start()

    logstash.info("http info message")

    await logstash.stop()

    assert len(http_logs) == 0


@mark.asyncio
async def test_tcp_sender(logstash_tcp_server: int) -> None:
    logstash = TCPSender(
        host="0.0.0.0", port=logstash_tcp_server, service_name="test_service"
    )

    logstash.set_level(LogLevel.DEBUG)

    await logstash.start()

    logstash.log(LogLevel.DEBUG, "tpc log message")
    logstash.debug("tcp debug message")
    logstash.info("tcp info message")
    logstash.warning("tcp warning message")
    logstash.error("tcp error message")

    await logstash.stop()

    assert len(tcp_logs) == 5


class MockRemoteLogSender(BaseRemoteLogSender):
    def __init__(
        self,
        max_log_retry: int = 5,
        log_queue_size: int = 1000,
        failed_log_queue_size: int = 1000,
        on_log_recieved_callback: Callable[[RemoteLogRecord], SenderResponse]
        | None = None,
        default_return: SenderResponse | None = None,
    ) -> None:
        super().__init__(
            service_name="test",
            max_log_retry=max_log_retry,
            log_queue_size=log_queue_size,
            failed_log_queue_size=failed_log_queue_size,
        )

        self._on_log_recieved_callback = on_log_recieved_callback
        self._default_return = default_return

    async def _send(self, log: RemoteLogRecord) -> SenderResponse:
        if self._on_log_recieved_callback is not None:
            return self._on_log_recieved_callback(log)

        return self._default_return or SenderResponse(
            sent=False, reason="no reason"
        )


@mark.asyncio
async def test_remote_logger_logs() -> None:
    loop = get_running_loop()
    log_future = loop.create_future()

    def on_log_recieved(log: RemoteLogRecord) -> SenderResponse:
        log_future.set_result(log)

        return SenderResponse(sent=True)

    remote_logger = MockRemoteLogSender(
        on_log_recieved_callback=on_log_recieved
    )

    await remote_logger.start()

    remote_logger.info(
        message="test_massage",
        tags=["tag_one", "tag_two"],
        extra={"extra_one": "value_one"},
    )

    log = await log_future

    assert isinstance(log, RemoteLogRecord)
    assert log.message == "test_massage"
    assert log.tags == ["tag_one", "tag_two"]
    assert log.labels == {"extra_one": "value_one"}


@mark.asyncio
async def test_remote_logger_log_retries() -> None:
    loop = get_running_loop()
    log_future = loop.create_future()

    def on_log_recieved(log: RemoteLogRecord) -> SenderResponse:
        if log.log_retries < 5:
            return SenderResponse(sent=False, reason="for testing reasons")

        log_future.set_result(log)

        return SenderResponse(sent=True)

    remote_logger = MockRemoteLogSender(
        max_log_retry=6, on_log_recieved_callback=on_log_recieved
    )

    await remote_logger.start()

    remote_logger.info(
        message="test_massage",
        tags=["tag_one", "tag_two"],
        extra={"extra_one": "value_one"},
    )

    log = await log_future

    assert isinstance(log, RemoteLogRecord)
    assert log.message == "test_massage"
    assert log.tags == ["tag_one", "tag_two"]
    assert log.labels == {"extra_one": "value_one"}
    assert log.log_retries == 5


@mark.asyncio
async def test_remote_logger_log_retries_with_exceptions() -> None:
    loop = get_running_loop()
    log_future = loop.create_future()

    def on_log_recieved(log: RemoteLogRecord) -> SenderResponse:
        if log.log_retries < 5:
            return SenderResponse(sent=False, reason="for testing reasons")

        log_future.set_result(log)

        return SenderResponse(sent=True)

    remote_logger = MockRemoteLogSender(
        max_log_retry=6, on_log_recieved_callback=on_log_recieved
    )

    await remote_logger.start()

    remote_logger.error(
        message="test_massage",
        tags=["tag_one", "tag_two"],
        extra={"extra_one": "value_one"},
        exception=ValueError("value_error"),
    )

    log = await log_future

    assert isinstance(log, RemoteLogRecord)
    assert log.message == "test_massage"
    assert log.tags == ["tag_one", "tag_two"]
    assert log.labels == {"extra_one": "value_one"}
    assert log.error == ("ValueError", "value_error", None)
    assert log.log_retries == 5


def test_remote_logger_log_record_properties() -> None:
    log = RemoteLogRecord(
        message="test remote logger log message",
        service_name="test",
        log_level=LogLevel.DEBUG,
        log_logger="MockLogger",
    )

    assert log.service_name == "test"
    assert log.log_level == LogLevel.DEBUG
    assert log.log_logger == "MockLogger"
    assert str(log) == "level `DEBUG`, message `test remote logger log message`"
    assert (
        repr(log)
        == "RemoteLogRecord (\n\tlevel : `DEBUG`,\n\tmessage : `test remote logger log message`,\n\ttags : [],\n\tlabel : {},\n\terror_type : `None`,\n\terror_message: `None`\n)"
    )


def test_remote_logger_log_exception_causes() -> None:
    def generate_cause(depth: int) -> ValueError:
        if depth <= 1:
            return ValueError(f"exception cause {depth}")

        e = ValueError(f"exception cause {depth}")
        e.__cause__ = generate_cause(depth - 1)

        return e

    log = RemoteLogRecord(
        message="test message",
        service_name="test",
        log_level=LogLevel.DEBUG,
        log_logger="MockRemoteLogSender",
    )

    e = Exception("main exception")
    e.__cause__ = generate_cause(10)
    log.error_from_exception(e)

    assert log.labels is not None
    assert log._error_type == "Exception"
    assert "causeOne" in log.labels
    assert log.labels["causeOne"] == "ValueError"
    assert "causeN" in log.labels
    assert log.labels["causeN"] == "ValueError"


def test_remote_logger_log_exception_contexts() -> None:
    def generate_context(depth: int) -> ValueError:
        if depth <= 1:
            return ValueError(f"exception context {depth}")

        e = ValueError(f"exception context {depth}")
        e.__context__ = generate_context(depth - 1)

        return e

    log = RemoteLogRecord(
        message="test message",
        service_name="test",
        log_level=LogLevel.DEBUG,
        log_logger="MockRemoteLogSender",
    )

    e = Exception("main exception")
    e.__cause__ = generate_context(10)
    log.error_from_exception(e)

    assert log.labels is not None
    assert log._error_type == "Exception"
    assert "causeOne" in log.labels
    assert log.labels["causeOne"] == "ValueError"
    assert "causeN" in log.labels
    assert log.labels["causeN"] == "ValueError"


def test_remote_logger_log_record_dict() -> None:
    remote_logger = BaseLogstashSender(service_name="test")
    log = RemoteLogRecord(
        message="test logstash message",
        service_name="test",
        log_level=LogLevel.DEBUG,
        log_logger="BaseLogstashSender",
    )

    log.tags = ["tag_one"]
    log.labels = {"extra_one": "value_one"}

    try:
        raise ValueError("value exception")
    except ValueError as e:
        log.error_from_exception(e)

    log_dict = remote_logger.remote_log_record_to_ecs(log)

    assert log_dict["message"] == "test logstash message"
    assert log_dict["service.name"] == "test"
    assert log_dict["log.level"] == "debug"
    assert log_dict["log.logger"] == "BaseLogstashSender"
    assert log_dict["tags"] == ["tag_one"]
    assert log_dict["labels"] == {"extra_one": "value_one"}
    assert log_dict["error.type"] == "ValueError"
    assert log_dict["error.message"] == "value exception"
    assert "error.stack_trace" in log_dict


@mark.asyncio
async def test_remote_logger_too_many_log_retries() -> None:
    loop = get_running_loop()
    log_retries_done = loop.create_future()

    def logger(log: RemoteLogRecord) -> SenderResponse:
        if log.log_retries == 3:
            log_retries_done.set_result(log.log_retries)

        return SenderResponse(sent=False, reason="no reason")

    remote_logger = MockRemoteLogSender(
        max_log_retry=4, on_log_recieved_callback=logger
    )

    await remote_logger.start()
    remote_logger.info("test log")

    assert await log_retries_done == 3


@mark.asyncio
async def test_remote_logger_send_exception() -> None:
    loop = get_running_loop()
    log_retries_done = loop.create_future()

    def logger(log: RemoteLogRecord) -> SenderResponse:
        if log.log_retries == 0:
            raise ValueError()

        log_retries_done.set_result(log)
        return SenderResponse(sent=True)

    remote_logger = MockRemoteLogSender(
        max_log_retry=1, on_log_recieved_callback=logger
    )

    await remote_logger.start()
    remote_logger.info("test log")

    log = await log_retries_done

    assert log.log_retries == 1


@mark.asyncio
async def test_remote_logger_exception_logger() -> None:
    loop = get_running_loop()
    exception_log_done = loop.create_future()

    def logger(log: RemoteLogRecord) -> SenderResponse:
        exception_log_done.set_result(log.error)

        return SenderResponse(sent=True)

    remote_logger = MockRemoteLogSender(on_log_recieved_callback=logger)

    await remote_logger.start()

    try:
        raise ValueError("value error")
    except:
        remote_logger.exception("exception logger")

    error_type, error_message, error_stack_trace = await exception_log_done

    assert error_type == "ValueError"
    assert error_message == "value error"
    assert error_stack_trace is not None


@mark.asyncio
async def test_remote_logger_stop_hook_exception() -> None:
    class MockRemoteLogSender(BaseRemoteLogSender):
        def __init__(self) -> None:
            super().__init__(service_name="test")

        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            return SenderResponse(sent=True)

        def _hook_on_stop(self) -> None:
            raise ValueError("hook on stop exception")

    remote_logger = MockRemoteLogSender()

    await remote_logger.start()

    with raises(ValueError) as exception_info:
        await remote_logger.stop()

    assert str(exception_info.value) == "hook on stop exception"


@mark.asyncio
async def test_remote_logger_stop_hook_async_exception() -> None:
    class MockRemoteLogSender(BaseRemoteLogSender):
        def __init__(self) -> None:
            super().__init__(service_name="test")

        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            return SenderResponse(sent=True)

        async def _hook_on_stop_async(self) -> None:
            raise ValueError("hook on stop exception")

    remote_logger = MockRemoteLogSender()

    await remote_logger.start()

    with raises(ValueError) as exception_info:
        await remote_logger.stop()

    assert str(exception_info.value) == "hook on stop exception"


@mark.asyncio
async def test_remote_logger_closed_failed_log_queue() -> None:
    loop = get_running_loop()
    failed_log_done = loop.create_future()
    logged_count = 0

    def logger(log: RemoteLogRecord) -> SenderResponse:
        nonlocal logged_count

        logged_count += 1

        failed_log_done.set_result(logged_count)

        return SenderResponse(sent=False, reason="testing reason")

    remote_logger = MockRemoteLogSender(on_log_recieved_callback=logger)

    await remote_logger.start()

    remote_logger.info("info log")

    await remote_logger.stop()

    assert await failed_log_done > 0
