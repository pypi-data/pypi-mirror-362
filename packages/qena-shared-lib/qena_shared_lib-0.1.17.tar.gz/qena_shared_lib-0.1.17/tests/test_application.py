from contextlib import asynccontextmanager
from logging import DEBUG
from typing import Annotated, Any, AsyncGenerator, Callable, Literal

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pytest import mark, raises

from qena_shared_lib.application import Builder, Environment
from qena_shared_lib.dependencies import Container
from qena_shared_lib.dependencies.http import DependsOn, get_service
from qena_shared_lib.exceptions import (
    BadRequest,
    HTTPServiceError,
    InternalServerError,
    Severity,
)
from qena_shared_lib.http import (
    ROUTE_HANDLER_ATTRIBUTE,
    ControllerBase,
    RouteHandlerMeta,
    api_controller,
    delete,
    get,
    head,
    options,
    patch,
    post,
    put,
    trace,
)
from qena_shared_lib.logging import LoggerProvider
from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    RemoteLogRecord,
    SenderResponse,
)


def test_application_builder() -> None:
    class ApplicationDependency:
        def __init__(self) -> None:
            self._status = "PENDING"

        def start(self) -> None:
            self._status = "RUNNING"

        def stop(self) -> None:
            self._status = "STOPPED"

        @property
        def status(self) -> str:
            return self._status

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        dependency = get_service(app=app, service_key=ApplicationDependency)

        assert isinstance(dependency, ApplicationDependency)

        dependency.start()

        yield

        dependency.stop()

    app = (
        Builder()
        .with_title("Test fastapi title")
        .with_description("Test fastapi description")
        .with_version("0.2.0")
        .with_environment(Environment.PRODUCTION)
        .with_lifespan(lifespan)
        .with_singleton(ApplicationDependency)
        .build()
    )

    assert isinstance(app, FastAPI)
    assert app.title == "Test fastapi title"
    assert app.description == "Test fastapi description"
    assert app.version == "0.2.0"

    dependency = get_service(app=app, service_key=ApplicationDependency)

    assert isinstance(dependency, ApplicationDependency)
    assert dependency.status == "PENDING"

    with TestClient(app) as _:
        assert dependency.status == "RUNNING"

    assert dependency.status == "STOPPED"


def test_application_development_environment() -> None:
    app = Builder().with_environment(Environment.DEVELOPMENT).build()

    assert app.debug == True

    with TestClient(app) as client:
        res = client.get("/openapi.json")

        assert res.is_success

        res = client.get("/docs")

        assert res.is_success

        res = client.get("/redoc")

        assert res.is_success


def test_application_production_environment() -> None:
    app = Builder().with_environment(Environment.PRODUCTION).build()

    assert app.debug == False

    with TestClient(app) as client:
        res = client.get("/openapi.json")

        assert res.status_code == 404

        res = client.get("/docs")

        assert res.status_code == 404

        res = client.get("/redoc")

        assert res.status_code == 404


@mark.asyncio
async def test_application_exception_handler() -> None:
    class TestRemoteLogSender(BaseRemoteLogSender):
        pass

    app = (
        Builder()
        .with_default_exception_handlers()
        .with_singleton(
            BaseRemoteLogSender,
            instance=TestRemoteLogSender("test_application"),
        )
        .with_singleton(LoggerProvider)
        .build()
    )

    logger_provider = get_service(app=app, service_key=LoggerProvider)
    logger = logger_provider.get_logger("test")

    logger.setLevel(DEBUG)

    @app.get("/{exception_type}")
    def service_exception_raiser(
        exception_type: Literal["service_exception", "general_exception"],
    ) -> None:
        match exception_type:
            case "service_exception":
                raise BadRequest("Service exception")
            case "general_exception":
                raise ValueError("General exception")

    with TestClient(app) as client:
        service_exception_response = client.get("/service_exception")

        assert service_exception_response.json() == {
            "severity": "MEDIUM",
            "message": "Service exception",
        }

        with raises(ValueError):
            _ = client.get("/general_exception")

        request_validation_error_response = client.get(
            "/request_validation_error"
        )

        request_validation_error_response_json = (
            request_validation_error_response.json()
        )
        assert request_validation_error_response_json["severity"] == "MEDIUM"
        assert (
            request_validation_error_response_json["message"]
            == "invalid request data"
        )
        assert request_validation_error_response_json["code"] == 100


@mark.asyncio
async def test_application_service_exception_handler_serverity() -> None:
    class TestRemoteLogSender(BaseRemoteLogSender):
        pass

    app = (
        Builder()
        .with_default_exception_handlers()
        .with_singleton(
            BaseRemoteLogSender,
            instance=TestRemoteLogSender("test_application"),
        )
        .with_singleton(LoggerProvider)
        .build()
    )

    @app.get("/{severity}")
    def service_exception_raiser(severity: int) -> None:
        match severity:
            case 0:
                raise HTTPServiceError(
                    message="Low severity exception", severity=Severity.LOW
                )
            case 1:
                raise BadRequest("Medium severity exception")
            case 2:
                raise InternalServerError("High severity exception")

    with TestClient(app) as client:
        client_error_response = client.get("/0")

        assert client_error_response.json() == {
            "severity": "LOW",
            "message": "Low severity exception",
        }

        server_error_response = client.get("/1")

        assert server_error_response.json() == {
            "severity": "MEDIUM",
            "message": "Medium severity exception",
        }

        server_error_response = client.get("/2")

        assert server_error_response.json() == {
            "severity": "HIGH",
            "message": "something went wrong",
        }


@mark.asyncio
async def test_application_exception_handler_with_header() -> None:
    class TestRemoteLogSender(BaseRemoteLogSender):
        pass

    app = (
        Builder()
        .with_default_exception_handlers()
        .with_singleton(
            BaseRemoteLogSender,
            instance=TestRemoteLogSender("test_application"),
        )
        .with_singleton(LoggerProvider)
        .build()
    )

    @app.get("/")
    def service_exception_raiser() -> None:
        raise InternalServerError(
            "server error", headers={"test_header": "test_header_value"}
        )

    with TestClient(app) as client:
        server_error_response = client.get("/")

        assert server_error_response.json() == {
            "severity": "HIGH",
            "message": "something went wrong",
        }
        assert "test_header" in server_error_response.headers
        assert (
            server_error_response.headers["test_header"] == "test_header_value"
        )


def test_api_controller() -> None:
    @api_controller("/test")
    class TestController(ControllerBase):
        @get()
        def get_route_handler(self) -> str:
            return "get_route_handler_response"

        @put()
        def put_route_handler(self, body: dict[str, Any]) -> str:
            return f"put_route_handler_reponse_{body['message']}"

        @post()
        def post_route_handler(self, body: dict[str, Any]) -> str:
            return f"post_route_handler_response_{body['message']}"

        @delete()
        def delete_route_handler(self) -> str:
            return "delete_route_handler_response"

        @options()
        def options_route_handler(self) -> str:
            return "options_route_handler_response"

        @head()
        def head_route_handler(self) -> str:
            return "head_route_handler_response"

        @patch()
        def patch_route_handler(self) -> str:
            return "patch_route_handler_response"

        @trace()
        def trace_route_handler(self) -> str:
            return "trace_route_handler_response"

    app = Builder().with_controllers(TestController).build()

    with TestClient(app) as client:
        res = client.get("/test")

        assert res.json() == "get_route_handler_response"

        res = client.put("/test", json={"message": "put_test_message"})

        assert res.json() == "put_route_handler_reponse_put_test_message"

        res = client.post("/test", json={"message": "post_test_message"})

        assert res.json() == "post_route_handler_response_post_test_message"

        res = client.delete("/test")

        assert res.json() == "delete_route_handler_response"

        res = client.options("/test")

        assert res.json() == "options_route_handler_response"

        res = client.head("/test")

        assert res.is_success

        res = client.patch("/test")

        assert res.json() == "patch_route_handler_response"


def test_api_controller_with_no_controller_base() -> None:
    @api_controller("/test")  # type: ignore
    class TestController:
        @get()
        def get_test_response(self) -> str:
            return "test_controller_response"

        @post()
        def post_test_response(self, body: dict[str, Any]) -> str:
            return f"test_controller_response_{body['message']}"

    with raises(TypeError):
        Builder().with_controllers([TestController])  # type: ignore

    with raises(TypeError):
        Builder().with_controllers(["str"])  # type: ignore

    with raises(TypeError):
        Builder().with_controllers([0])  # type: ignore


def test_api_controller_with_no_api_controller() -> None:
    class TestController(ControllerBase):
        @get()
        def get_test_response(self) -> str:
            return "test_controller_response"

        @post()
        def post_test_response(self, body: dict[str, Any]) -> str:
            return f"test_controller_response_{body['message']}"

    with raises(AttributeError):
        _ = Builder().with_controllers(TestController).build()


def test_api_controller_with_no_wrong_method_annotation() -> None:
    def wrong_get() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            setattr(func, ROUTE_HANDLER_ATTRIBUTE, "wrong_value")

            return func

        return wrapper

    @api_controller("/test")
    class TestController(ControllerBase):
        @wrong_get()
        def get_test_response(self) -> str:
            return "test_controller_response"

        @post()
        def post_test_response(self, body: dict[str, Any]) -> str:
            return f"test_controller_response_{body['message']}"

    with raises(TypeError):
        _ = Builder().with_controllers(TestController).build()


def test_api_controller_with_unknown_method() -> None:
    def wrong_get() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            setattr(
                func,
                ROUTE_HANDLER_ATTRIBUTE,
                RouteHandlerMeta(
                    method="CUSTOMER"  # type: ignore
                ),
            )

            return func

        return wrapper

    @api_controller("/test")
    class TestController(ControllerBase):
        @wrong_get()
        def get_test_response(self) -> str:
            return "test_controller_response"

        @post()
        def post_test_response(self, body: dict[str, Any]) -> str:
            return f"test_controller_response_{body['message']}"

    with raises(ValueError):
        _ = Builder().with_controllers(TestController).build()


def test_wrong_api_router() -> None:
    class WrongAPIRouter:
        pass

    with raises(TypeError) as exception_info:
        Builder().with_routers([WrongAPIRouter])  # type: ignore

    exception_value = exception_info.value

    assert str(exception_value) == "some routers are not type `APIRouter`"


def test_routers() -> None:
    router = APIRouter(prefix="/users")

    @router.get("")
    def get_users() -> list[str]:
        return ["user_one", "user_two"]

    app = Builder().with_routers(router).build()

    with TestClient(app) as client:
        res = client.get("/users")

        assert res.json() == ["user_one", "user_two"]


def test_transient_service() -> None:
    class TransientService:
        def __init__(self) -> None:
            self._value = 0

        @property
        def value(self) -> int:
            return self._value

        @value.setter
        def value(self, value: int) -> None:
            self._value = value

    router = APIRouter(prefix="/values")

    @router.get("")
    def get_value(
        transient_service: Annotated[
            TransientService, DependsOn(TransientService)
        ],
    ) -> int:
        return transient_service.value

    @router.post("")
    def set_value(
        value: int,
        transient_service: Annotated[
            TransientService, DependsOn(TransientService)
        ],
    ) -> None:
        transient_service.value = value

    app = (
        Builder().with_transient(TransientService).with_routers(router).build()
    )

    with TestClient(app) as client:
        _ = client.post("/values", params={"value": 10})
        res = client.get("/values")

        assert res.json() == 0


def test_environment() -> None:
    builder = Builder()

    builder.with_environment(Environment.DEVELOPMENT)

    assert builder.environment == Environment.DEVELOPMENT

    builder.with_environment(Environment.PRODUCTION)

    assert builder.environment == Environment.PRODUCTION


def test_countainer() -> None:
    class SingltonService:
        pass

    singlton_service = SingltonService()
    builder = Builder().with_singleton(
        SingltonService, instance=singlton_service
    )
    container = builder.container

    assert isinstance(container, Container)
    assert singlton_service == container.resolve(SingltonService)


@mark.asyncio
async def test_none_remote_logging() -> None:
    router = APIRouter(prefix="/users")

    @router.get("")
    def get_users(severity: int) -> None:
        match severity:
            case 0:
                raise HTTPServiceError(
                    message="low serverity",
                    severity=Severity.LOW,
                    remote_logging=False,
                )
            case 1:
                raise HTTPServiceError(
                    message="medium severity",
                    severity=Severity.MEDIUM,
                    body={"field_one": "value_one"},
                    response_code=0,
                    corrective_action="nothing",
                    remote_logging=False,
                )
            case 2:
                raise HTTPServiceError(
                    message="high serverity",
                    severity=Severity.HIGH,
                    tags=["tag_one"],
                    extra={"extra_one": "value_one"},
                    remote_logging=False,
                )

    log_count = 0

    class MockLogSender(BaseRemoteLogSender):
        def __init__(self) -> None:
            super().__init__(service_name="test")

        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            nonlocal log_count

            log_count += 1

            return SenderResponse(sent=True)

    app = (
        Builder()
        .with_default_exception_handlers()
        .with_singleton(service=BaseRemoteLogSender, factory=MockLogSender)
        .with_singleton(LoggerProvider)
        .with_routers(router)
        .build()
    )

    remote_logger = get_service(app=app, service_key=BaseRemoteLogSender)

    await remote_logger.start()

    with TestClient(app) as client:
        res = client.get("/users", params={"severity": 0})

        await remote_logger.stop()

        assert res.status_code == 400
        assert res.json() == {"severity": "LOW", "message": "low serverity"}
        assert log_count == 0

        await remote_logger.start()

        res = client.get("/users", params={"severity": 1})

        await remote_logger.stop()

        assert res.status_code == 400
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "medium severity",
            "code": 0,
            "correctiveAction": "nothing",
            "field_one": "value_one",
        }
        assert log_count == 0

        await remote_logger.start()

        res = client.get("/users", params={"severity": 2})

        await remote_logger.stop()

        assert res.status_code == 500
        assert res.json() == {
            "severity": "HIGH",
            "message": "something went wrong",
        }
        assert log_count == 0


def test_service_exception_repr() -> None:
    generic_service_exception = HTTPServiceError("Service exception")

    assert repr(generic_service_exception).startswith(
        "HTTPServiceError ( message: `Service exception`"
    )

    bad_request_exception = BadRequest("Bad request exception")

    assert repr(bad_request_exception).startswith(
        "BadRequest ( message: `Bad request exception`"
    )
