from datetime import datetime, timedelta
from typing import Annotated

from fastapi.testclient import TestClient
from pytest import mark

from qena_shared_lib.application import Builder
from qena_shared_lib.http import ControllerBase, api_controller, get
from qena_shared_lib.logging import LoggerProvider
from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    RemoteLogRecord,
    SenderResponse,
)
from qena_shared_lib.security import (
    Authorization,
    JwtAdapter,
    PermissionMatch,
    UserInfo,
    get_int_from_datetime,
    jwk_from_dict,
)


class MockRemoteLogSender(BaseRemoteLogSender):
    async def _send(self, _: RemoteLogRecord) -> SenderResponse:
        return SenderResponse(sent=True)


@mark.asyncio
async def test_endpoint_acl_expired_token() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[UserInfo, Authorization()],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        admin_token = await JwtAdapter().encode(
            payload={
                "userId": "1",
                "type": "admin",
                "exp": get_int_from_datetime(
                    datetime.now() - timedelta(hours=1)
                ),
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_client_error
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_invalid_payload() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[UserInfo, Authorization()],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        admin_token = await JwtAdapter().encode(
            payload={
                "iss": "test",
                "sub": "test",
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_client_error
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_any_user_type() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[UserInfo, Authorization()],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_specific_user_type() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[UserInfo, Authorization(user_type="admin")],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_any_user_type_some_permissions() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[
                UserInfo, Authorization(permissions=["READ", "WRITE"])
            ],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "admin",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["DELETE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["DELETE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_specific_user_type_some_permissions() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[
                UserInfo,
                Authorization(user_type="admin", permissions=["READ", "WRITE"]),
            ],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "admin",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["DELETE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["DELETE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_any_user_type_all_permissions() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[
                UserInfo,
                Authorization(
                    permissions=["READ", "WRITE"],
                    permission_match_strategy=PermissionMatch.ALL,
                ),
            ],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "admin",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["DELETE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["DELETE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }


@mark.asyncio
async def test_endpoint_acl_specific_user_type_all_permissions() -> None:
    @api_controller(prefix="/users")
    class UsersController(ControllerBase):
        @get()
        def get_users(
            self,
            _: Annotated[
                UserInfo,
                Authorization(
                    user_type="admin",
                    permissions=["READ", "WRITE"],
                    permission_match_strategy=PermissionMatch.ALL,
                ),
            ],
        ) -> list[str]:
            return ["user_1", "user_2"]

    jwt_adapter = JwtAdapter()
    remote_logger = MockRemoteLogSender("test_service")
    app = (
        Builder()
        .with_singleton(LoggerProvider)
        .with_singleton(JwtAdapter, instance=jwt_adapter)
        .with_singleton(BaseRemoteLogSender, instance=remote_logger)
        .with_controllers(UsersController)
        .with_default_exception_handlers()
        .build()
    )

    with TestClient(app) as client:
        test_jwt_adapter = JwtAdapter()
        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "admin",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.is_success
        assert res.json() == ["user_1", "user_2"]

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        admin_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "admin", "permissions": ["DELETE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": admin_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["READ"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": ["WRITE"]},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["READ", "WRITE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client"},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={"userId": "1", "type": "client", "permissions": []},
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        client_token = await test_jwt_adapter.encode(
            payload={
                "userId": "1",
                "type": "client",
                "permissions": ["DELETE"],
            },
            key=jwk_from_dict({"kty": "oct", "k": ""}),
        )
        res = client.get("/users", headers={"authorization": client_token})

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }

        res = client.get("/users")

        assert res.status_code == 401
        assert res.json() == {
            "severity": "MEDIUM",
            "message": "you are not authorized to access requested resource",
            "code": 0,
        }
