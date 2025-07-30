# Qena shared lib

A shared tools for other services. It includes.

- FastAPI app builder
- A wrapper around fastapi to make it class based.
- RabbitMQ utility class to listen, respond, publish and make rpc request.
- Remote logging
    - Logstash utility class to log message in `ecs` ( elastic common schema ).
- A simple task scheduler, to schedule task to run in specific time.
- Background task runner.
- Security tools ( password hasher, jwt, acl ).
- IOC container to manager dependencies used across fastapi, rabbitmq manager and schedule manager.

# Usage

## Environment variables

- `QENA_SHARED_LIB_LOGGING_LOGGER_NAME` root logger name.
- `QENA_SHARED_LIB_SECURITY_UNAUTHORIZED_RESPONSE_CODE` an integer response on an authorized access of resource.
- `QENA_SHARED_LIB_SECURITY_TOKEN_HEADER` to header key for jwt token.

## Http

To create fastapi app.

``` py
from qena_shared_lib.application import Builder, Environment


def main() -> FastAPI:
    builder = (
        Builder()
        .with_title("Qena shared lib")
        .with_description("A shared tools for other services.")
        .with_version("0.1.0")
        .with_environment(Environment.PRODUCTION)
        .with_default_exception_handlers()
    )

    app = builder.build()

    return app
```

To run app

``` sh
$ uvicorn --factory main:main
```

### Lifespan

``` py
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
def lifespan(app: FastAPI):
    ...

    yield

    ...


def main() -> FastAPI:
    ...

    builder.with_lifespan(lifespan)

    ...
```

### Dependencies

``` py
class EmailService:
    def __init__(self):
        ...


class Database:
    def __init__(self):
        ...


def main() -> FastAPI:
    ...

    builder.with_singleton(EmailService)
    builder.with_transient(Database)

    ...
```

### Controllers

``` py
from qena_shared_lib.http import ControllerBase, api_controller, post


@api_controller("/users")
class UserController(ControllerBase):

    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    @post()
    async def send_email(self, message: str):
        await self._email_service.send(message)


def main() -> FastAPI:
    ...

    builder.with_controllers(UserController)

    ...
```

### Routers

``` py
from fastapi import APIRouter

from qena_shared_lib.dependencies.http import DependsOn


router = APIRouter(prefix="/auth")


@router.post("")
async def login(
    db: Annotated[Database, DependsOn(Database)],
    username: str,
    password: str
):
    ...


def main() -> FastAPI:
    ...

    builder.with_routers(router)

    ...
```

To enable metrics.

``` py
def main() -> FastAPI:
    ...

    builder.with_metrics()

    ...
```

## Remote logging

### Logstash
``` py
from qena_shared_lib.remotelogging import BaseRemoteLogSender
from qena_shared_lib.remotelogging.logstash import HTTPSender, # TCPSender


@asynccontextmanager
async def lifespan(app: FastAPI):
    remote_logger = get_service(BaseRemoteLogSender)

    await remote_logger.start()

    yield

    await remote_logger.stop()


def main() -> FastAPI:
    ...

    remote_logger = HTTPSender(
        service_name="qena-shared-lib",
        url="http://127.0.0.1:18080",
        user="logstash",
        password="logstash",
    )
    # or
    # remote_logger = TCPSender(
    #   service_name="qena-shared-lib",
    #   host="127.0.0.1",
    #   port=18090
    # )
    builder.with_singleton(
        service=BaseRemoteLogSender,
        instance=remote_logger,
    )

    ...


@router.get("")
def log_message(
    remote_logger: Annotated[
        BaseRemoteLogSender,
        DependsOn(BaseRemoteLogSender),
    ],
    message: str,
):
    remote_logger.info(message)
```

## Rabbitmq

To create rabbitmq connection manager.

``` py
from qena_shared_lib.rabbitmq import ListenerBase, consume, consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = get_service(RabbitMqManager)

    await rabbitmq.connect()

    yield

    rabbitmq.disconnect()


@consumer("UserQueue")
class UserConsumer(ListenerBase):

    def __init__(self, db: Database):
        self._db = db

    @consume()
    async def store_user(self, user: User):
        await self._db.save(user)


def main() -> FastAPI:
    ...

    rabbitmq = RabbitMqManager(
        remote_logger=remote_logger,
        container=builder.container,
    )

    rabbitmq.init_default_exception_handlers()
    rabbitmq.include_listener(UserConsumer)
    builder.add_singleton(
        service=RabbitMqManager,
        instance=rabbitmq,
    )

    ...
```

### Publisher

``` py
@router.post("")
async def store_user(
    rabbitmq: Annotated[
        RabbitMqManager,
        DependsOn(RabbitMqManager)
    ],
    user: User,
)
    publisher = rabbitmq.publisher("UserQueue")

    await publisher.publish(user)
    # await publisher.publish_as_arguments(user)
```

### RPC client

``` py
@router.get("")
async def get_user(
    rabbitmq: Annotated[
        RabbitMqManager,
        DependsOn(RabbitMqManager)
    ],
    user_id: str,
)
    rpc_client = rabbitmq.rpc_client("UserQueue")

    user = await rpc_client.call(user_id)
    # user = await rpc_client.call_with_arguments(user_id)

    return user
```

### Flow control

``` py
from qena_shared_lib.rabbitmq import ... , ListenerContext


@consumer("UserQueue")
class UserConsumer(ListenerBase):

    @consume()
    async def store_user(self, ctx: ListenerContext, user: User):
        ...

        await ctx.flow_control.request(10)

        ...

```

### Rpc reply

Optionally it is possible to reply to rpc calls, through.

``` py
from qena_shared_lib.rabbitmq import ... , rpc_worker


@rpc_worker("UserQueue")
class UserWorker(ListenerBase):

    @execute()
    async def store_user(self, ctx: ListenerContext, user: User):
        ...

        await ctx.rpc_reply.reply("Done")

        ...
```

### Retry consumer

Consumer can retry to consumer a message in an event of failure.

``` py
from qena_shared_lib.rabbitmq import (
    BackoffRetryDelay,
    FixedRetryDelay,
    RabbitMqManager,
    RetryDelayJitter,
    RetryPolicy,
)


@consumer(
    queue="UserQueue",
    # can be defined for consumer of specific queue
    retry_policy=RetryPolicy(
        exceptions=(AMQPError,),
        max_retry=5,
        retry_delay_strategy=FixedRetryDelay(
            retry_delay=2
        ),
        retry_delay_jitter=RetryDelayJitter(min=0.5, max=5.0),
    )
)
class UserConsumer(ListenerBase):

    @consume(
        # for specific target
        retry_policy=RetryPolicy(
            exceptions=(AMQPError,),
            max_retry=5,
            retry_delay_strategy=FixedRetryDelay(
                retry_delay=2
            ),
            retry_delay_jitter=RetryDelayJitter(min=0.5, max=5.0),
        )
    )
    async def store_user(self, ctx: ListenerContext, user: User):
        ...

        await ctx.flow_control.request(10)

        ...


def main() -> FastAPI:
    ...

    rabbitmq = RabbitMqManager(
        remote_logger=remote_logger,
        container=builder.container,
        # or globally for all consumers
        listener_global_retry_policy=RetryPolicy(
            exceptions=(AMQPError,),
            max_retry=10,
            retry_delay_strategy=BackoffRetryDelay(
                multiplier=1.5, min=2, max=10
            ),
            retry_delay_jitter=RetryDelayJitter(min=0.5, max=5.0),
            match_by_cause=True,
        ),
    )

    rabbitmq.include_listener(UserConsumer)
    builder.add_singleton(
        service=RabbitMqManager,
        instance=rabbitmq,
    )
```



## Scheduler

``` py
from qena_shared_lib.scheduler import (
    ScheduleManager,
    # Scheduler,
    SchedulerBase,
    schedule,
    scheduler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    schedule_manager = get_service(ScheduleManager)

    rabbitmq.start()

    yield

    schedule_manager.stop()


@scheduler()
class TaskScheduler(SchedulerBase):

    def __init__(self, db: Database)

    @schedule("* * * * *")
    def do_task(
        self,

    ):
        ...
# or
# scheduler = Scheduler()

# @scheduler.schedule("* * * * *")
# def do_task(
#     db: Annotated[Database, DependsOn(Database)]
# ):
#     ...


def main() -> FastAPI:
    ...

    schedule_manager = ScheduleManager(
        remote_logger=remote_logger,
        container=builder.container
    )

    schedule_manager.include_scheduler(TaskScheduler)
    builder.with_singleton(
        service=ScheduleManager,
        instance=schedule_manager,
    )

    ...
```

## Background

``` py
from qena_shared_lib.background import Background


@asynccontextmanager
async def lifespan(app: FastAPI):
    background = get_service(Background)

    background.start()

    yield

    background.stop()


def main() -> FastAPI:
    ...

    builder.with_singleton(
        service=BaseRemoteLogSender,
        instance=remote_logger,
    )
    builder.with_singleton(Background)

    ...


async def data_processor(data: Data):
    ...


@router.get("")
async def process_data(
    background: Annotated[
        Background,
        DependsOne(Background)
    ],
    data: Data
)
    background.add_task(BackgroundTask(data_processor, data))
```

## Security

### Password hasher

``` py
from qena_shared_lib.security import PasswordHasher


@api_controller("/users")
class UserController(ControllerBase):

    def __init__(self, password_hasher: PasswordHasher):
        self._password_hasher = password_hasher

    @post()
    async def signup(self, user: User):
        await self._password_hasher.hash(user.password)

    @post()
    async def login(self, user: User):
        await self._password_hasher.verify(user.password)


def main() -> FastAPI:
    ...

    builder.with_singleton(PasswordHasher)
    builder.with_controllers([
        UserController
    ])

    ...
```

### JWT

``` py
from qena_shared_lib.security import JwtAdapter


@ApiController("/users")
class UserController(ControllerBase):

    def __init__(
        self,

        ...

        jwt: JwtAdapter,
    ):
        ...

        self._jwt = jwt

    @post()
    async def login(self, user: User):
        payload = { ... }

        await self._jwt.encode(payload)

    @post
    async def verifiy(self, token: str):
        await self._jwt.decode(token)


def main() -> FastAPI:
    ...

    builder.with_singleton(JwtAdapter)
    builder.with_controllers([
        UserController
    ])

    ...
```

### ACL

``` py
from qena_shared_lib.security import Authorization


@api_controller("/users")
class UserController(ControllerBase):

    @post()
    async def get_user(
        self,
        user: Annotated[
            UserInfo,
            Authorization(
                user_type="ADMIN",
                persmissions=[
                    "READ"
                ],
            )
        ]
    ):
        ...


@router.get("")
async def get_users(
    user: Annotated[
        UserInfo,
        Authorization("ADMIN")
    ]
)
    ...
```
