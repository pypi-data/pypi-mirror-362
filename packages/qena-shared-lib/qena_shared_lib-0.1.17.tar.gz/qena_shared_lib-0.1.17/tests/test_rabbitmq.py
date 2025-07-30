from asyncio import Future, Queue, Task, gather, get_running_loop, sleep
from typing import Annotated, Any, Callable, Generator, cast

from pika.adapters.asyncio_connection import AsyncioConnection
from pika.exceptions import ProbableAuthenticationError
from pydantic import BaseModel, EmailStr, ValidationError
from pytest import fixture, mark, raises
from testcontainers.rabbitmq import RabbitMqContainer

from qena_shared_lib.dependencies import (
    Container,
    MissingDependencyError,
    Scope,
)
from qena_shared_lib.dependencies.miscellaneous import DependsOn
from qena_shared_lib.exceptions import (
    RabbitMQConnectionUnhealthyError,
    RabbitMQRpcRequestPendingError,
    RabbitMQRpcRequestTimeoutError,
    RabbitMQServiceException,
    ServiceException,
    Severity,
)
from qena_shared_lib.logging import LoggerProvider
from qena_shared_lib.rabbitmq import (
    LISTENER_ATTRIBUTE,
    AbstractRabbitMqExceptionHandler,
    AbstractRabbitMQService,
    BackoffRetryDelay,
    BaseChannel,
    ChannelPool,
    Consumer,
    FixedRetryDelay,
    ListenerBase,
    ListenerContext,
    RabbitMqManager,
    RetryDelayJitter,
    RetryPolicy,
    RpcWorker,
    consume,
    consumer,
    execute,
    rpc_worker,
)
from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    LogLevel,
    RemoteLogRecord,
    SenderResponse,
)
from qena_shared_lib.utils import AsyncEventLoopMixin


@fixture(scope="module")
def rabbitmq() -> Generator[RabbitMqContainer, None, None]:
    rabbitmq_container = RabbitMqContainer("rabbitmq:4.0.3-management")

    rabbitmq_container.with_name("test_rabbitmq")
    rabbitmq_container.start()

    yield rabbitmq_container

    rabbitmq_container.stop()


@mark.asyncio
async def test_rabbitmq_connection_manager(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()


@mark.asyncio
async def test_rabbitmq_connection_manager_wrong_listeners(
    remote_logger: BaseRemoteLogSender,
) -> None:
    class WrongListener:
        pass

    rabbitmq_connector = RabbitMqManager(remote_logger=remote_logger)

    with raises(TypeError):
        rabbitmq_connector.include_listener(WrongListener())  # type: ignore

    with raises(TypeError):
        rabbitmq_connector.include_listener(WrongListener)  # type: ignore

    with raises(TypeError):
        rabbitmq_connector.include_listener(1)  # type: ignore


@mark.asyncio
async def test_rabbitmq_connection_management_wrong_inner_listener(
    remote_logger: BaseRemoteLogSender,
) -> None:
    class NoInnerListener(ListenerBase):
        pass

    def wrong_listener() -> Callable[[type[ListenerBase]], type[ListenerBase]]:
        def wrapper(listner: type[ListenerBase]) -> type[ListenerBase]:
            setattr(listner, LISTENER_ATTRIBUTE, object())

            return listner

        return wrapper

    @wrong_listener()
    class WrongInnerListener(ListenerBase):
        pass

    rabbit_mq_manager = RabbitMqManager(remote_logger=remote_logger)

    with raises(AttributeError):
        rabbit_mq_manager.include_listener(NoInnerListener)

    with raises(TypeError):
        rabbit_mq_manager.include_listener(WrongInnerListener)


@mark.asyncio
async def test_rabbitmq_wrong_service(
    remote_logger: BaseRemoteLogSender,
) -> None:
    class WrongRabbitMQService:
        pass

    rabbit_mq_manager = RabbitMqManager(remote_logger=remote_logger)

    with raises(TypeError) as exception_info:
        rabbit_mq_manager.include_service(WrongRabbitMQService)  # type: ignore

        exception_value = exception_info.value

        assert str(exception_value).startswith(
            "rabbitmq service is not type of `AbstractRabbitMQService`,"
        )

    with raises(TypeError) as exception_info:
        rabbit_mq_manager.include_service(WrongRabbitMQService())  # type: ignore

        exception_value = exception_info.value

        assert str(exception_value).startswith(
            "rabbitmq service is not type of `AbstractRabbitMQService`,"
        )


@mark.asyncio
async def test_rabbitmq_access_disconnected_connection(
    remote_logger: BaseRemoteLogSender,
) -> None:
    rabbit_mq_manager = RabbitMqManager(remote_logger=remote_logger)

    with raises(RabbitMQConnectionUnhealthyError) as exception_info:
        rabbit_mq_manager.connection

        exception_value = exception_info.value

        assert str(exception_value) == "connection not ready yet"


@mark.asyncio
async def test_rabbitmq_disconnect_unconnected_connection(
    remote_logger: BaseRemoteLogSender,
) -> None:
    rabbit_mq_manager = RabbitMqManager(remote_logger=remote_logger)

    with raises(RabbitMQConnectionUnhealthyError) as exception_info:
        await rabbit_mq_manager.disconnect()

        exception_value = exception_info.value

        assert str(exception_value) == "connection not ready yet"


@mark.asyncio
async def test_rabbitmq_access_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbit_mq_manager = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbit_mq_manager.connect()

    assert rabbit_mq_manager.connection is not None


@mark.asyncio
async def test_rabbitmq_string_parameter(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    host = rabbitmq.get_container_host_ip()
    port = rabbitmq.get_exposed_port(rabbitmq.port)
    username = rabbitmq.username
    password = rabbitmq.password
    rabbitmq_connector = RabbitMqManager(
        parameters=f"amqp://{username}:{password}@{host}:{port}/%2F",
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.disconnect()


@mark.asyncio
async def test_rabbitmq_failed_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    host = rabbitmq.get_container_host_ip()
    port = rabbitmq.get_exposed_port(rabbitmq.port)
    rabbit_mq_manager = RabbitMqManager(
        parameters=f"amqp://wrong_user:wrong_password@{host}:{port}/%2F",
        remote_logger=remote_logger,
    )

    with raises(ProbableAuthenticationError):
        await rabbit_mq_manager.connect()


@mark.asyncio
async def test_rabbitmq_publisher(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    publisher = rabbitmq_connector.publisher("publisher_test_queue")

    await publisher.publish_as_arguments()
    await publisher.publish_as_arguments("message")
    await publisher.publish_as_arguments(
        message_one="message_one", message_two="message_two"
    )
    await publisher.publish()
    await publisher.publish("message")
    await rabbitmq_connector.disconnect()


@mark.asyncio
async def test_rabbitmq_publisher_with_no_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    with raises(RabbitMQConnectionUnhealthyError):
        _ = rabbitmq_connector.publisher(
            "publisher_with_no_connection_test_queue"
        )


@mark.asyncio
async def test_rabbitmq_publisher_on_disconnected_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    _ = rabbitmq_connector.publisher(
        "publisher_on_disconnected_connection_test_queue"
    )

    await rabbitmq_connector.disconnect()

    with raises(RabbitMQConnectionUnhealthyError):
        _ = rabbitmq_connector.publisher(
            "publisher_on_disconnected_connection_test_queue"
        )


@mark.asyncio
async def test_rabbitmq_rpc_client(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_client_test_queue", timeout=0.1
    )

    with raises(RabbitMQRpcRequestTimeoutError):
        await rpc_client.call()

    with raises(RabbitMQRpcRequestTimeoutError):
        await rpc_client.call("message")

    with raises(RabbitMQRpcRequestTimeoutError):
        await rpc_client.call_with_arguments(
            message_one="message_one", message_two="message_two"
        )

    with raises(RabbitMQRpcRequestTimeoutError):
        await rpc_client.call()

    with raises(RabbitMQRpcRequestTimeoutError):
        await rpc_client.call("message")

    await rabbitmq_connector.disconnect()


@mark.asyncio
async def test_simultaneous_rabbitmq_rpc_client_call(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    loop = get_running_loop()
    first_rpc_call_future = loop.create_future()
    second_rpc_call_future = loop.create_future()
    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_client_test_queue", timeout=0.1
    )

    def rpc_call_done(call: str, task: Task[Any]) -> None:
        e = task.exception()

        if e is None:
            first_rpc_call_future.set_exception(
                RuntimeError("e task doesn't have exception")
            )

            return

        if call == "first":
            first_rpc_call_future.set_exception(e)
        elif call == "second":
            second_rpc_call_future.set_exception(e)

    loop.create_task(rpc_client.call("first")).add_done_callback(
        lambda task: rpc_call_done("first", task)
    )
    loop.create_task(rpc_client.call("second")).add_done_callback(
        lambda task: rpc_call_done("second", task)
    )

    with raises(RabbitMQRpcRequestPendingError):
        await second_rpc_call_future

    with raises(RabbitMQRpcRequestTimeoutError):
        await first_rpc_call_future

    await rabbitmq_connector.disconnect()


@mark.asyncio
async def test_rabbitmq_rpc_client_with_no_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    with raises(RabbitMQConnectionUnhealthyError):
        _ = rabbitmq_connector.rpc_client(
            "rpc_client_with_no_connection_test_queue"
        )


@mark.asyncio
async def test_rabbitmq_rpc_client_on_disconnected_connection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    _ = rabbitmq_connector.publisher(
        "rpc_client_on_disconnected_connection_test_queue"
    )

    await rabbitmq_connector.disconnect()

    with raises(RabbitMQConnectionUnhealthyError):
        _ = rabbitmq_connector.publisher(
            "rpc_client_on_disconnected_connection_test_queue"
        )


@mark.asyncio
async def test_rabbitmq_gracefull_shutdown(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_recieved_future = loop.create_future()
    exited = False
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer = Consumer("gracefull_shutdown_test_queue")

    @consumer.consume()
    async def message_consumer() -> None:
        nonlocal exited

        consumer_recieved_future.set_result(None)
        await sleep(0)

        exited = True

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "gracefull_shutdown_test_queue"
    ).publish_as_arguments()
    await consumer_recieved_future
    await rabbitmq_connector.disconnect()

    assert exited


@mark.asyncio
async def test_rabbitmq_consumer(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future_one = loop.create_future()
    consumer_future_two = loop.create_future()
    consumer = Consumer("consumer_test_queue")

    @consumer.consume()
    def message_consumer(message: str) -> None:
        match message:
            case "first":
                consumer_future_one.set_result(True)
            case "second":
                consumer_future_two.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    publisher = rabbitmq_connector.publisher("consumer_test_queue")

    await publisher.publish_as_arguments("first")
    await publisher.publish("second")

    assert all(await gather(consumer_future_one, consumer_future_two))


@mark.asyncio
async def test_rabbitmq_consumer_arguments(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    no_args = loop.create_future()
    positional_args = loop.create_future()
    keyword_args = loop.create_future()
    positional_and_keyword_args = loop.create_future()
    consumer = Consumer("consumer_arguments_test_queue")

    @consumer.consume("no_args")
    def no_args_consumer() -> None:
        no_args.set_result(None)

    @consumer.consume("positional_args")
    def positional_args_consumer(*args: str) -> None:
        positional_args.set_result(args)

    @consumer.consume("keyword_args")
    def keyword_args_consumer(**kwargs: str) -> None:
        keyword_args.set_result(kwargs)

    @consumer.consume("positional_and_keyword_args")
    def positional_and_keyword_args_consumer(*args: str, **kwargs: str) -> None:
        positional_and_keyword_args.set_result((args, kwargs))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    await rabbitmq_connector.publisher(
        "consumer_arguments_test_queue", target="no_args"
    ).publish_as_arguments()
    await rabbitmq_connector.publisher(
        "consumer_arguments_test_queue", target="positional_args"
    ).publish_as_arguments("positional_arg_message")
    await rabbitmq_connector.publisher(
        "consumer_arguments_test_queue", target="keyword_args"
    ).publish_as_arguments(keyword_arg="keyword_arg_message")
    await rabbitmq_connector.publisher(
        "consumer_arguments_test_queue", target="positional_and_keyword_args"
    ).publish_as_arguments(
        "positional_arg_message", keyword_arg="keyword_arg_message"
    )

    assert await no_args is None
    assert await positional_args == ("positional_arg_message",)
    assert await keyword_args == {"keyword_arg": "keyword_arg_message"}
    assert await positional_and_keyword_args == (
        ("positional_arg_message",),
        {"keyword_arg": "keyword_arg_message"},
    )


@mark.asyncio
async def test_rabbitmq_consumer_argument_parsing(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    positional_args = loop.create_future()
    keyword_args = loop.create_future()
    consumer = Consumer("consumer_argument_parsing_test_queue")

    @consumer.consume("positional_args")
    def positional_args_consumer(arg_one: int, arg_two: float) -> None:
        positional_args.set_result(
            isinstance(arg_one, int) and isinstance(arg_two, float)
        )

    @consumer.consume("keyword_args")
    def keyword_args_consumer(arg_one: int, arg_two: float) -> None:
        keyword_args.set_result(
            isinstance(arg_one, int) and isinstance(arg_two, float)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    await rabbitmq_connector.publisher(
        "consumer_argument_parsing_test_queue", target="positional_args"
    ).publish_as_arguments(80, 100.20)
    await rabbitmq_connector.publisher(
        "consumer_argument_parsing_test_queue", target="keyword_args"
    ).publish_as_arguments(arg_one=80, arg_two=100.20)

    assert await positional_args
    assert await keyword_args


@mark.asyncio
async def test_rabbitmq_consumer_none_python_argument_parsing(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    none_python_argument = loop.create_future()
    consumer = Consumer("consumer_argument_none_python_parsing_test_queue")

    @consumer.consume()
    def none_python_argument_consumer(argument: int) -> None:
        none_python_argument.set_result(argument)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_argument_none_python_parsing_test_queue"
    ).publish(10)

    assert await none_python_argument == 10


@mark.asyncio
async def test_rabbitmq_consumer_single_arg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    single_arg_future = loop.create_future()
    consumer = Consumer("consumer_single_arg_test_queue")

    @consumer.consume()
    def single_arg_consumer(arg_one: int, /) -> None:
        single_arg_future.set_result(arg_one)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_single_arg_test_queue"
    ).publish_as_arguments(10)

    assert await single_arg_future == 10


@mark.asyncio
async def test_rabbitmq_consumer_single_kwarg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    single_kwarg_future = loop.create_future()
    consumer = Consumer("consumer_single_kwarg_test_queue")

    @consumer.consume()
    def single_kwarg_consumer(*, kwarg_one: int) -> None:
        single_kwarg_future.set_result(kwarg_one)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_single_kwarg_test_queue"
    ).publish_as_arguments(kwarg_one=10)

    assert await single_kwarg_future == 10


@mark.asyncio
async def test_rabbitmq_consumer_multiple_arg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    multiple_arg_future = loop.create_future()
    consumer = Consumer("consumer_multiple_arg_test_queue")

    @consumer.consume()
    def multiple_arg_consumer(arg_one: int, arg_two: int, /) -> None:
        multiple_arg_future.set_result((arg_one, arg_two))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_multiple_arg_test_queue"
    ).publish_as_arguments(10, 20)

    assert await multiple_arg_future == (10, 20)


@mark.asyncio
async def test_rabbitmq_consumer_multiple_kwarg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    multiple_kwarg_future = loop.create_future()
    consumer = Consumer("consumer_multiple_kwarg_test_queue")

    @consumer.consume()
    def multiple_kwarg_consumer(*, kwarg_one: int, kwarg_two: int) -> None:
        multiple_kwarg_future.set_result((kwarg_one, kwarg_two))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_multiple_kwarg_test_queue"
    ).publish_as_arguments(kwarg_one=10, kwarg_two=20)

    assert await multiple_kwarg_future == (10, 20)


@mark.asyncio
async def test_rabbitmq_consumer_single_arg_and_kwarg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    single_arg_and_kwarg_future = loop.create_future()
    consumer = Consumer("consumer_single_arg_and_kwarg_test_queue")

    @consumer.consume()
    def single_arg_and_kwarg_consumer(arg_one: int, *, kwarg_one: int) -> None:
        single_arg_and_kwarg_future.set_result((arg_one, kwarg_one))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_single_arg_and_kwarg_test_queue"
    ).publish_as_arguments(10, kwarg_one=20)

    assert await single_arg_and_kwarg_future == (10, 20)


@mark.asyncio
async def test_rabbitmq_consumer_multiple_arg_and_kwarg(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    multiple_arg_and_kwarg_future = loop.create_future()
    consumer = Consumer("consumer_multiple_arg_and_kwarg_test_queue")

    @consumer.consume()
    def multiple_arg_and_kwarg_consumer(
        arg_one: int, arg_two: int, *, kwarg_one: int, kwarg_two: int
    ) -> None:
        multiple_arg_and_kwarg_future.set_result(
            (arg_one, arg_two, kwarg_one, kwarg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_multiple_arg_and_kwarg_test_queue"
    ).publish_as_arguments(10, 20, kwarg_one=30, kwarg_two=40)

    assert await multiple_arg_and_kwarg_future == (10, 20, 30, 40)


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_dependency_at_the_begining(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_dependency_at_the_begining_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_dependency_at_the_begining_test_queue"
    )

    class ConsumerDependency:
        pass

    @consumer.consume()
    def arg_with_dependency_at_the_begining_consumer(
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        arg_one: int,
        /,
    ) -> None:
        arg_with_dependency_at_the_begining_future.set_result(
            (dep_one, arg_one)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_dependency_at_the_begining_test_queue"
    ).publish_as_arguments(10)

    assert await arg_with_dependency_at_the_begining_future == (
        consumer_dependency,
        10,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_multiple_dependency_at_the_begining(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_multiple_dependency_at_the_begining_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_multiple_dependency_at_the_begining_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def arg_with_multiple_dependency_at_the_begining_consumer(
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
        arg_one: int,
        /,
    ) -> None:
        arg_with_multiple_dependency_at_the_begining_future.set_result(
            (dep_one, dep_two, arg_one)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_multiple_dependency_at_the_begining_test_queue"
    ).publish_as_arguments(10)

    assert await arg_with_multiple_dependency_at_the_begining_future == (
        consumer_dependency_one,
        consumer_dependency_two,
        10,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_dependency_at_the_end(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_dependency_at_the_end_future = loop.create_future()
    consumer = Consumer("consumer_arg_with_dependency_at_the_end_test_queue")

    class ConsumerDependency:
        pass

    @consumer.consume()
    def arg_with_dependency_at_the_end_consumer(
        arg_one: int,
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        /,
    ) -> None:
        arg_with_dependency_at_the_end_future.set_result((arg_one, dep_one))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_dependency_at_the_end_test_queue"
    ).publish_as_arguments(10)

    assert await arg_with_dependency_at_the_end_future == (
        10,
        consumer_dependency,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_multiple_dependency_at_the_end(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_multiple_dependency_at_the_end_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_multiple_dependency_at_the_end_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def arg_with_multiple_dependency_at_the_end_consumer(
        arg_one: int,
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
        /,
    ) -> None:
        arg_with_multiple_dependency_at_the_end_future.set_result(
            (arg_one, dep_one, dep_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_multiple_dependency_at_the_end_test_queue"
    ).publish_as_arguments(10)

    assert await arg_with_multiple_dependency_at_the_end_future == (
        10,
        consumer_dependency_one,
        consumer_dependency_two,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_multiple_dependency_in_the_middle(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_multiple_dependency_in_the_middle_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_multiple_dependency_in_the_middle_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def arg_with_multiple_dependency_in_the_middle_consumer(
        arg_one: int,
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
        arg_two: int,
        /,
    ) -> None:
        arg_with_multiple_dependency_in_the_middle_future.set_result(
            (arg_one, dep_one, dep_two, arg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_multiple_dependency_in_the_middle_test_queue"
    ).publish_as_arguments(10, 20)

    assert await arg_with_multiple_dependency_in_the_middle_future == (
        10,
        consumer_dependency_one,
        consumer_dependency_two,
        20,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_dependency_in_the_middle(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_dependency_in_the_middle_future = loop.create_future()
    consumer = Consumer("consumer_arg_with_dependency_in_the_middle_test_queue")

    class ConsumerDependency:
        pass

    @consumer.consume()
    def arg_with_dependency_in_the_middle_consumer(
        arg_one: int,
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        arg_two: int,
        /,
    ) -> None:
        arg_with_dependency_in_the_middle_future.set_result(
            (arg_one, dep_one, arg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_dependency_in_the_middle_test_queue"
    ).publish_as_arguments(10, 20)

    assert await arg_with_dependency_in_the_middle_future == (
        10,
        consumer_dependency,
        20,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_dependency_at_the_begining(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_dependency_at_the_begining_future = loop.create_future()
    consumer = Consumer(
        "consumer_kwarg_with_dependency_at_the_begining_test_queue"
    )

    class ConsumerDependency:
        pass

    @consumer.consume()
    def kwarg_with_dependency_at_the_begining_consumer(
        *,
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        kwarg_one: int,
    ) -> None:
        kwarg_with_dependency_at_the_begining_future.set_result(
            (dep_one, kwarg_one)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_dependency_at_the_begining_test_queue"
    ).publish_as_arguments(kwarg_one=10)

    assert await kwarg_with_dependency_at_the_begining_future == (
        consumer_dependency,
        10,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_multiple_dependency_at_the_begining(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_multiple_dependency_at_the_begining_future = loop.create_future()
    consumer = Consumer(
        "consumer_kwarg_with_multiple_dependency_at_the_begining_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def kwarg_with_multiple_dependency_at_the_begining_consumer(
        *,
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
        kwarg_one: int,
    ) -> None:
        kwarg_with_multiple_dependency_at_the_begining_future.set_result(
            (dep_one, dep_two, kwarg_one)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_multiple_dependency_at_the_begining_test_queue"
    ).publish_as_arguments(kwarg_one=10)

    assert await kwarg_with_multiple_dependency_at_the_begining_future == (
        consumer_dependency_one,
        consumer_dependency_two,
        10,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_dependency_at_the_end(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_dependency_at_the_end_future = loop.create_future()
    consumer = Consumer("consumer_kwarg_with_dependency_at_the_end_test_queue")

    class ConsumerDependency:
        pass

    @consumer.consume()
    def kwarg_with_dependency_at_the_end_consumer(
        *,
        kwarg_one: int,
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
    ) -> None:
        kwarg_with_dependency_at_the_end_future.set_result((kwarg_one, dep_one))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_dependency_at_the_end_test_queue"
    ).publish_as_arguments(kwarg_one=10)

    assert await kwarg_with_dependency_at_the_end_future == (
        10,
        consumer_dependency,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_multiple_dependency_at_the_end(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_multiple_dependency_at_the_end_future = loop.create_future()
    consumer = Consumer(
        "consumer_kwarg_with_multiple_dependency_at_the_end_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def kwarg_with_multiple_dependency_at_the_end_consumer(
        *,
        kwarg_one: int,
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
    ) -> None:
        kwarg_with_multiple_dependency_at_the_end_future.set_result(
            (kwarg_one, dep_one, dep_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_multiple_dependency_at_the_end_test_queue"
    ).publish_as_arguments(kwarg_one=10)

    assert await kwarg_with_multiple_dependency_at_the_end_future == (
        10,
        consumer_dependency_one,
        consumer_dependency_two,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_dependency_in_the_middle(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_dependency_in_the_middle_future = loop.create_future()
    consumer = Consumer(
        "consumer_kwarg_with_dependency_in_the_middle_test_queue"
    )

    class ConsumerDependency:
        pass

    @consumer.consume()
    def kwarg_with_dependency_in_the_middle_consumer(
        *,
        kwarg_one: int,
        dep_one: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        kwarg_two: int,
    ) -> None:
        kwarg_with_dependency_in_the_middle_future.set_result(
            (kwarg_one, dep_one, kwarg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependency, instance=consumer_dependency
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_dependency_in_the_middle_test_queue"
    ).publish_as_arguments(kwarg_one=10, kwarg_two=20)

    assert await kwarg_with_dependency_in_the_middle_future == (
        10,
        consumer_dependency,
        20,
    )


@mark.asyncio
async def test_rabbitmq_consumer_kwarg_with_multiple_dependency_in_the_middle(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    kwarg_with_multiple_dependency_in_the_middle_future = loop.create_future()
    consumer = Consumer(
        "consumer_kwarg_with_multiple_dependency_in_the_middle_test_queue"
    )

    class ConsumerDependencyOne:
        pass

    class ConsumerDependencyTwo:
        pass

    @consumer.consume()
    def kwarg_with_multiple_dependency_in_the_middle_consumer(
        *,
        kwarg_one: int,
        dep_one: Annotated[
            ConsumerDependencyOne, DependsOn(ConsumerDependencyOne)
        ],
        dep_two: Annotated[
            ConsumerDependencyTwo, DependsOn(ConsumerDependencyTwo)
        ],
        kwarg_two: int,
    ) -> None:
        kwarg_with_multiple_dependency_in_the_middle_future.set_result(
            (kwarg_one, dep_one, dep_two, kwarg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency_one = ConsumerDependencyOne()
    consumer_dependency_two = ConsumerDependencyTwo()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        service=ConsumerDependencyOne, instance=consumer_dependency_one
    )
    rabbitmq_connector.container.register(
        service=ConsumerDependencyTwo, instance=consumer_dependency_two
    )

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_kwarg_with_multiple_dependency_in_the_middle_test_queue"
    ).publish_as_arguments(kwarg_one=10, kwarg_two=20)

    assert await kwarg_with_multiple_dependency_in_the_middle_future == (
        10,
        consumer_dependency_one,
        consumer_dependency_two,
        20,
    )


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_listener_context_at_the_begining(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_listener_context_at_the_begining_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_listener_context_at_the_begining_test_queue"
    )

    @consumer.consume()
    def arg_with_listener_context_at_the_begining_consumer(
        ctx: ListenerContext,
        arg_one: int,
        /,
    ) -> None:
        arg_with_listener_context_at_the_begining_future.set_result(
            (ctx, arg_one)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_listener_context_at_the_begining_test_queue"
    ).publish_as_arguments(10)

    ctx, arg_one = await arg_with_listener_context_at_the_begining_future

    assert isinstance(ctx, ListenerContext)
    assert (
        ctx.queue
        == "consumer_arg_with_listener_context_at_the_begining_test_queue"
    )
    assert ctx.listener_name == "__default__"
    assert arg_one == 10


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_listener_context_at_the_end(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_listener_context_at_the_end_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_listener_context_at_the_end_test_queue"
    )

    @consumer.consume()
    def arg_with_listener_context_at_the_end_consumer(
        kwarg_one: int,
        ctx: ListenerContext,
        /,
    ) -> None:
        arg_with_listener_context_at_the_end_future.set_result((kwarg_one, ctx))

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_listener_context_at_the_end_test_queue"
    ).publish_as_arguments(10)

    arg_one, ctx = await arg_with_listener_context_at_the_end_future

    assert arg_one == 10
    assert isinstance(ctx, ListenerContext)
    assert (
        ctx.queue == "consumer_arg_with_listener_context_at_the_end_test_queue"
    )
    assert ctx.listener_name == "__default__"


@mark.asyncio
async def test_rabbitmq_consumer_arg_with_listener_context_in_the_middle(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    arg_with_listener_context_in_the_middle_future = loop.create_future()
    consumer = Consumer(
        "consumer_arg_with_listener_context_in_the_middle_test_queue"
    )

    @consumer.consume()
    def arg_with_listener_context_in_the_middle_consumer(
        arg_one: int,
        ctx: ListenerContext,
        arg_two: int,
        /,
    ) -> None:
        arg_with_listener_context_in_the_middle_future.set_result(
            (arg_one, ctx, arg_two)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_arg_with_listener_context_in_the_middle_test_queue"
    ).publish_as_arguments(10, 20)

    arg_one, ctx, arg_two = await arg_with_listener_context_in_the_middle_future

    assert arg_one == 10
    assert isinstance(ctx, ListenerContext)
    assert (
        ctx.queue
        == "consumer_arg_with_listener_context_in_the_middle_test_queue"
    )
    assert ctx.listener_name == "__default__"
    assert arg_two == 20


@mark.asyncio
async def test_rabbitmq_reconnection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consume_future = loop.create_future()
    consumer = Consumer("consumer_reconnection_test_queue")

    @consumer.consume()
    def payload_consumer(payload: str) -> None:
        consume_future.set_result("test payload")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        reconnect_delay=0.1,
        reconnect_delay_jitter=(0.0, 0.1),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    rabbitmq.exec(
        f'rabbitmqctl close_all_user_connections {rabbitmq.username} "testing reason"'
    )
    rabbitmq.exec(
        'rabbitmqadmin publish exchange=amq.default routing_key=consumer_reconnection_test_queue payload="test payload"'
    )

    assert await consume_future == "test payload"


@mark.asyncio
async def test_consumer_global_retry_policy(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future = loop.create_future()
    consumer = Consumer("consumer_global_retry_policy_test_queue")
    retries = 0

    @consumer.consume()
    def message_consumer() -> None:
        nonlocal retries

        if retries < 2:
            retries += 1
            raise ValueError()

        consumer_future.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=2,
            retry_delay_strategy=FixedRetryDelay(0.1),
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_global_retry_policy_test_queue"
    ).publish_as_arguments()

    assert await consumer_future and retries == 2


@mark.asyncio
async def test_local_consumer_retry_policy(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future = loop.create_future()
    consumer = Consumer(
        queue="consumer_local_retry_policy_test_queue",
        retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=2,
            retry_delay_strategy=FixedRetryDelay(0.1),
        ),
    )
    retries = 0

    @consumer.consume()
    def message_consumer() -> None:
        nonlocal retries

        if retries < 2:
            retries += 1
            raise ValueError()

        consumer_future.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=4,
            retry_delay_strategy=FixedRetryDelay(0.1),
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_local_retry_policy_test_queue"
    ).publish_as_arguments()

    assert await consumer_future and retries == 2


@mark.asyncio
async def test_consumer_retry_policy(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future = loop.create_future()
    consumer = Consumer(
        queue="consumer_retry_policy_test_queue",
        retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=4,
            retry_delay_strategy=FixedRetryDelay(0.1),
        ),
    )
    retries = 0

    @consumer.consume(
        retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=4,
            retry_delay_strategy=FixedRetryDelay(0.1),
        )
    )
    def message_consumer() -> None:
        nonlocal retries

        if retries < 2:
            retries += 1
            raise ValueError()

        consumer_future.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=1,
            retry_delay_strategy=FixedRetryDelay(0.1),
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_retry_policy_test_queue"
    ).publish_as_arguments()

    assert await consumer_future and retries == 2


@mark.asyncio
async def test_consumer_backoff_retry_delay_policy_wrong_range(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    with raises(ValueError) as exception_info:
        _ = RabbitMqManager(
            parameters=rabbitmq.get_connection_params(),
            listener_global_retry_policy=RetryPolicy(
                exceptions=(ValueError,),
                max_retry=2,
                retry_delay_strategy=BackoffRetryDelay(
                    multiplier=1.0, min=1.0, max=0.1
                ),
            ),
            remote_logger=remote_logger,
        )

    assert str(exception_info.value) == "`min` greater than `max`"


@mark.asyncio
async def test_consumer_backoff_retry_delay_policy(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future = loop.create_future()
    consumer = Consumer("consumer_backoff_retry_delay_policy_test_queue")
    retries = 0

    @consumer.consume()
    def message_consumer() -> None:
        nonlocal retries

        if retries < 2:
            retries += 1
            raise ValueError()

        consumer_future.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=2,
            retry_delay_strategy=BackoffRetryDelay(
                multiplier=1.0, min=0.0, max=0.1
            ),
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_backoff_retry_delay_policy_test_queue"
    ).publish_as_arguments()

    assert await consumer_future and retries == 2


@mark.asyncio
async def test_consumer_retry_delay_jitter_wrong_range(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    with raises(ValueError) as exception_info:
        _ = RabbitMqManager(
            parameters=rabbitmq.get_connection_params(),
            listener_global_retry_policy=RetryPolicy(
                exceptions=(ValueError,),
                max_retry=2,
                retry_delay_strategy=FixedRetryDelay(retry_delay=1.0),
                retry_delay_jitter=RetryDelayJitter(min=1.0, max=0.1),
            ),
            remote_logger=remote_logger,
        )

    assert str(exception_info.value) == "`min` greater than `max`"


@mark.asyncio
async def test_consumer_retry_policy_with_jitter(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future = loop.create_future()
    consumer = Consumer("consumer_retry_policy_with_jitter_test_queue")
    retries = 0

    @consumer.consume()
    def message_consumer() -> None:
        nonlocal retries

        if retries < 2:
            retries += 1
            raise ValueError()

        consumer_future.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=2,
            retry_delay_strategy=FixedRetryDelay(0.1),
            retry_delay_jitter=RetryDelayJitter(min=0.0, max=0.1),
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_retry_policy_with_jitter_test_queue"
    ).publish_as_arguments()

    assert await consumer_future and retries == 2


@mark.asyncio
async def test_consumer_retry_policy_exception_match_by_cause_or_context(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_cause_future = loop.create_future()
    consumer_context_future = loop.create_future()
    consumer = Consumer(
        "consumer_retry_policy_exception_match_by_cause_or_context_queue"
    )
    retries = 0

    class ExceptionForCause(Exception):
        pass

    class ExcptionForContext(Exception):
        pass

    @consumer.consume()
    def message_consumer(cause_or_context: str) -> None:
        nonlocal retries

        if retries == 2:
            match cause_or_context:
                case "cause":
                    consumer_cause_future.set_result(True)
                case _:
                    consumer_context_future.set_result(True)

            return

        try:
            raise ValueError()
        except ValueError as e:
            retries += 1

            match cause_or_context:
                case "cause":
                    raise ExceptionForCause() from e
                case _:
                    raise ExcptionForContext()

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        listener_global_retry_policy=RetryPolicy(
            exceptions=(ValueError,),
            max_retry=2,
            retry_delay_strategy=FixedRetryDelay(0.1),
            match_by_cause=True,
        ),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_retry_policy_exception_match_by_cause_or_context_queue"
    ).publish_as_arguments("cause")

    assert await consumer_cause_future and retries == 2

    retries = 0

    await rabbitmq_connector.publisher(
        "consumer_retry_policy_exception_match_by_cause_or_context_queue"
    ).publish_as_arguments("context")

    assert await consumer_context_future and retries == 2


@mark.asyncio
async def test_rabbitmq_rpc_worker(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    worker = RpcWorker("rpc_worker_test_queue")

    @worker.execute()
    def rpc_worker(message: str) -> str:
        match message:
            case "first":
                return "first_response"
            case "second":
                return "second_response"
            case _:
                return "other_response"

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()

    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_worker_test_queue",
        timeout=0.1,
    )
    first_response = await rpc_client.call_with_arguments("first")
    second_response = await rpc_client.call("second")

    assert (
        first_response == "first_response"
        and second_response == "second_response"
    )


@mark.asyncio
async def test_rabbitmq_rpc_worker_exception(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestRemoteLogSender(BaseRemoteLogSender):
        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            del log

            return SenderResponse(sent=True)

    worker = RpcWorker("rpc_worker_exception_test_queue")

    @worker.execute()
    def rpc_worker(message: str) -> None:
        match message:
            case "rabbitmq":
                raise RabbitMQServiceException(
                    code=10, message="rabbitmq_exception"
                )
            case _:
                raise ValueError("other_exception")

    container = Container()

    container.register(
        BaseRemoteLogSender, instance=TestRemoteLogSender("test_service")
    )
    container.register(LoggerProvider)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        container=container,
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(worker)
    rabbitmq_connector.init_default_exception_handlers()
    await rabbitmq_connector.connect()

    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_worker_exception_test_queue", timeout=0.1
    )

    with raises(RabbitMQServiceException) as exception_info:
        await rpc_client.call("rabbitmq")

        exception = exception_info.value

        assert exception.code == 10
        assert exception.message == "rabbitmq_exception"

    with raises(RabbitMQServiceException) as exception_info:
        await rpc_client.call("other")

        exception = exception_info.value

        assert exception.code == 0
        assert exception.message == "test_exception"


@mark.asyncio
async def test_simultaneous_rabbitmq_rpc_client_call_with_return_type(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    worker = RpcWorker("rpc_client_call_with_return_type_test_queue")

    @worker.execute()
    def rpc_worker(message: str, count: int) -> dict[str, int | str]:
        if count > 0:
            return {"count": count}

        return {"message": message}

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()

    class RpcCallResponse(BaseModel):
        message: str

    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_client_call_with_return_type_test_queue",
        return_type=RpcCallResponse,
        timeout=0.1,
    )

    response = await rpc_client.call_with_arguments("test message", 0)

    assert isinstance(response, RpcCallResponse)
    assert response.message == "test message"

    with raises(ValidationError):
        _ = await rpc_client.call_with_arguments("test message", 1)


@mark.asyncio
async def test_rabbitmq_consumer_exception_handler(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_value_error_handler_future = loop.create_future()
    consumer = Consumer("consumer_exception_handler_test_queue")

    @consumer.consume()
    def message_consumer() -> None:
        raise ValueError("value_error")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ValueErrorHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return cast(type[Exception], ValueError)

        def __call__(self, _: ListenerContext, error: ValueError) -> None:
            consumer_value_error_handler_future.set_exception(error)

    rabbitmq_connector.set_exception_handlers(ValueErrorHandler)
    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    await rabbitmq_connector.publisher(
        "consumer_exception_handler_test_queue"
    ).publish_as_arguments()

    with raises(ValueError):
        await consumer_value_error_handler_future


@mark.asyncio
async def test_rabbitmq_rpc_worker_exception_handler(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    rpc_worker_value_error_handler_future = loop.create_future()
    rpc_worker_rabbitmq_exception_handler_future = loop.create_future()
    worker = RpcWorker("rpc_worker_exception_handler_test_queue")

    @worker.execute()
    def rpc_worker(message: str) -> None:
        match message:
            case "rabbitmq":
                raise RabbitMQServiceException(
                    code=10, message="rabbitmq_exception"
                )
            case _:
                raise ValueError("other_exception")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ValueErrorHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return cast(type[Exception], ValueError)

        async def __call__(
            self, _: ListenerContext, exception: ValueError
        ) -> None:
            await sleep(0)
            rpc_worker_value_error_handler_future.set_exception(exception)

    class RabbitMQServiceExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return cast(type[Exception], RabbitMQServiceException)

        def __call__(
            self, _: ListenerContext, exception: RabbitMQServiceException
        ) -> None:
            rpc_worker_rabbitmq_exception_handler_future.set_exception(
                exception
            )

    rabbitmq_connector.set_exception_handlers(
        ValueErrorHandler, RabbitMQServiceExceptionHandler
    )
    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()

    rpc_client = rabbitmq_connector.rpc_client(
        routing_key="rpc_worker_exception_handler_test_queue", timeout=5
    )

    with raises(RabbitMQServiceException) as exception_info:
        await rpc_client.call("rabbitmq")

        assert exception_info.value.message == "rabbitmq_exception"

    with raises(RabbitMQServiceException) as exception_info:
        await rpc_client.call("unknown")

        assert exception_info.value.message == "other_exception"

    with raises(RabbitMQServiceException) as exception_info:
        await rpc_worker_rabbitmq_exception_handler_future

        assert exception_info.value.message == "rabbitmq_exception"

    with raises(ValueError):
        await rpc_worker_value_error_handler_future


@mark.asyncio
async def test_rabbitmq_validation_exception_handler(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    validation_exception_handler_future = loop.create_future()
    consumer = Consumer("validation_exception_handler_test_queue")

    class Payload(BaseModel):
        name: str
        email: EmailStr

    @consumer.consume()
    def message_consumer(_: Payload) -> None:
        pass

    class MockRemoteLogSender(BaseRemoteLogSender):
        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            validation_exception_handler_future.set_result(log.tags)

            return SenderResponse(sent=True)

    container = Container()
    mock_remote_logger = MockRemoteLogSender(service_name="test")

    container.register(
        service=BaseRemoteLogSender,
        scope=Scope.singleton,
        instance=mock_remote_logger,
    )
    container.register(service=LoggerProvider, scope=Scope.singleton)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        container=container,
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.init_default_exception_handlers()
    await mock_remote_logger.start()
    await rabbitmq_connector.connect()

    publisher = rabbitmq_connector.publisher(
        "validation_exception_handler_test_queue"
    )

    await publisher.publish_as_arguments({"name": 10})

    assert "ValidationError" in await validation_exception_handler_future


@mark.asyncio
async def test_rabbitmq_service_exception_handler(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    service_exception_handler_queue: Queue[RemoteLogRecord] = Queue()
    consumer = Consumer("service_exception_handler_test_queue")

    @consumer.consume()
    def message_consumer(severity: str) -> None:
        tags = [severity]
        extra = {"severity": severity}

        match severity.lower():
            case "low":
                raise ServiceException(
                    message="low severity exception",
                    severity=Severity.LOW,
                    tags=tags,
                    extra=extra,
                )
            case "medium":
                raise ServiceException(
                    message="medium severity exception",
                    severity=Severity.MEDIUM,
                    tags=tags,
                    extra=extra,
                )
            case _:
                raise ServiceException(
                    message="high severity exception",
                    severity=Severity.HIGH,
                    tags=tags,
                    extra=extra,
                )

    class MockRemoteLogSender(BaseRemoteLogSender):
        async def _send(self, log: RemoteLogRecord) -> SenderResponse:
            service_exception_handler_queue.put_nowait(log)

            return SenderResponse(sent=True)

    container = Container()
    mock_remote_logger = MockRemoteLogSender(service_name="test")

    container.register(
        service=BaseRemoteLogSender,
        scope=Scope.singleton,
        instance=mock_remote_logger,
    )
    container.register(service=LoggerProvider, scope=Scope.singleton)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        container=container,
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.init_default_exception_handlers()
    await mock_remote_logger.start()
    await rabbitmq_connector.connect()

    publisher = rabbitmq_connector.publisher(
        "service_exception_handler_test_queue"
    )

    await publisher.publish_as_arguments("low")

    log = await service_exception_handler_queue.get()

    assert isinstance(log, RemoteLogRecord)
    assert log.log_level == LogLevel.INFO
    assert log.tags is not None
    assert "low" in log.tags

    await publisher.publish_as_arguments("medium")

    log = await service_exception_handler_queue.get()

    assert isinstance(log, RemoteLogRecord)
    assert log.log_level == LogLevel.WARNING
    assert log.tags is not None
    assert "medium" in log.tags

    await publisher.publish_as_arguments("high")

    log = await service_exception_handler_queue.get()

    assert isinstance(log, RemoteLogRecord)
    assert log.log_level == LogLevel.ERROR
    assert log.tags is not None
    assert "high" in log.tags


@mark.asyncio
async def test_rabbitmq_consumer_all_exception_handler(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_exception_handler_future = loop.create_future()
    consumer = Consumer("consumer_all_exception_handler_test_queue")

    @consumer.consume()
    def message_consumer() -> None:
        raise ValueError("value_error")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return Exception

        def __call__(self, _: ListenerContext, exception: Exception) -> None:
            consumer_exception_handler_future.set_exception(exception)

    rabbitmq_connector.set_exception_handlers(ExceptionHandler)
    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    await rabbitmq_connector.publisher(
        "consumer_all_exception_handler_test_queue"
    ).publish_as_arguments()

    with raises(ValueError):
        await consumer_exception_handler_future


@mark.asyncio
async def test_rabbitmq_consumer_exception_handler_precedence(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_exception_handler_future = loop.create_future()
    consumer = Consumer("consumer_exception_handler_precedence_test_queue")

    @consumer.consume()
    def message_consumer(message: str) -> None:
        del message
        raise ValueError("value_error")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return Exception

        def __call__(self, _: ListenerContext, exception: Exception) -> None:
            consumer_exception_handler_future.set_result((Exception, exception))

    class ValueErrorHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return cast(type[Exception], ValueError)

        def __call__(self, _: ListenerContext, exception: ValueError) -> None:
            consumer_exception_handler_future.set_result(
                (ValueError, exception)
            )

    rabbitmq_connector.set_exception_handlers(
        ExceptionHandler, ValueErrorHandler
    )
    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()

    await rabbitmq_connector.publisher(
        "consumer_exception_handler_precedence_test_queue"
    ).publish_as_arguments()

    exception_type, exeception = await consumer_exception_handler_future

    assert exception_type is ValueError
    assert isinstance(exeception, ValueError)


@mark.asyncio
async def test_rabbitmq_consumer_dependency(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_future_one = loop.create_future()
    consumer_future_two = loop.create_future()
    consumer = Consumer("consumer_dependency_test_queue")

    class ConsumerSubDependency:
        def __init__(self) -> None:
            self._value: str | None = None

        @property
        def value(self) -> str:
            if self._value is None:
                raise ValueError()

            return self._value

        @value.setter
        def value(self, value: str) -> None:
            self._value = value

    class ConsumerDependency:
        def __init__(
            self, consumer_sub_dependency: ConsumerSubDependency
        ) -> None:
            self._consumer_sub_dependency = consumer_sub_dependency

        @property
        def consumer_sub_dependency(self) -> ConsumerSubDependency:
            return self._consumer_sub_dependency

    @consumer.consume()
    def message_consumer(
        some_dependency: Annotated[
            ConsumerDependency, DependsOn(ConsumerDependency)
        ],
    ) -> None:
        if not consumer_future_one.done():
            some_dependency.consumer_sub_dependency.value = "value_one"
            consumer_future_one.set_result(True)
        elif not consumer_future_two.done():
            some_dependency.consumer_sub_dependency.value = "value_two"
            consumer_future_two.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    consumer_sub_dependency = ConsumerSubDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        ConsumerSubDependency, instance=consumer_sub_dependency
    )
    rabbitmq_connector.container.register(ConsumerDependency)

    await rabbitmq_connector.connect()

    with raises(ValueError):
        consumer_sub_dependency.value

    publisher = rabbitmq_connector.publisher("consumer_dependency_test_queue")

    await publisher.publish_as_arguments()

    assert await consumer_future_one
    assert consumer_sub_dependency.value == "value_one"

    await publisher.publish_as_arguments()

    assert await consumer_future_two
    assert consumer_sub_dependency.value == "value_two"


@mark.asyncio
async def test_rabbitmq_consumer_none_python_argument_with_dependency(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    none_python_argument = loop.create_future()
    consumer = Consumer(
        "consumer_argument_none_python_with_dependency_test_queue"
    )

    class ConsumerDependency:
        pass

    @consumer.consume()
    def none_python_argument_consumer(
        _: Annotated[ConsumerDependency, DependsOn(ConsumerDependency)],
        argument: int,
    ) -> None:
        none_python_argument.set_result(argument)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(ConsumerDependency)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_argument_none_python_with_dependency_test_queue"
    ).publish(10)

    assert await none_python_argument == 10


@mark.asyncio
async def test_rabbitmq_consumer_dependency_exception(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_exception_future = loop.create_future()
    consumer = Consumer("consumer_dependency_exception_test_queue")

    class ConsumerDependency:
        pass

    @consumer.consume()
    def message_consumer(
        some_dependency: Annotated[
            ConsumerDependency, DependsOn(ConsumerDependency)
        ],
    ) -> None:
        del some_dependency

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return Exception

        def __call__(self, _: ListenerContext, exception: Exception) -> None:
            consumer_exception_future.set_exception(exception)

    rabbitmq_connector.set_exception_handlers(ExceptionHandler)
    rabbitmq_connector.include_listener(consumer)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_dependency_exception_test_queue"
    ).publish_as_arguments()

    with raises(MissingDependencyError):
        await consumer_exception_future


@mark.asyncio
async def test_rabbitmq_listener_exception_handler_dependency(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_exception_future = loop.create_future()
    consumer = Consumer("listener_exception_handler_dependency_test_queue")

    class ConsumerDependency:
        def __init__(self) -> None:
            self._value: int | None = None

        @property
        def value(self) -> int | None:
            return self._value

        @value.setter
        def value(self, value: int) -> None:
            self._value = value

    @consumer.consume()
    def message_consumer(
        some_dependency: Annotated[
            ConsumerDependency, DependsOn(ConsumerDependency)
        ],
    ) -> None:
        some_dependency.value = 10
        raise ValueError()

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )
    consumer_dependency = ConsumerDependency()

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.container.register(
        ConsumerDependency, instance=consumer_dependency
    )

    class ExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return Exception

        def __init__(self, consumer_dependency: ConsumerDependency):
            self._consumer_dependency = consumer_dependency

        def __call__(self, _: ListenerContext, exception: Exception) -> None:
            self._consumer_dependency.value = (
                consumer_dependency.value or 0
            ) + 10
            consumer_exception_future.set_exception(exception)

    rabbitmq_connector.set_exception_handlers(ExceptionHandler)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "listener_exception_handler_dependency_test_queue"
    ).publish_as_arguments()

    with raises(ValueError):
        await consumer_exception_future

    assert consumer_dependency.value == 20


@mark.asyncio
async def test_rabbitmq_listener_exception_handler_parameter(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ExceptionHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return Exception

        def __call__(
            self, context: ListenerContext, exception: Exception
        ) -> None:
            del context, exception

    rabbitmq_connector.set_exception_handlers(ExceptionHandler)
    await rabbitmq_connector.connect()


@mark.asyncio
async def test_rabbitmq_listener_listener_context_parameter(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_listener_context_received = loop.create_future()
    rpc_worker_listener_context_received = loop.create_future()
    consumer = Consumer("consumer_listener_context_parameter_test_queue")
    worker = RpcWorker("rpc_worker_listener_context_parameter_test_queue")

    @consumer.consume()
    def message_consumer(context: ListenerContext) -> None:
        consumer_listener_context_received.set_result(
            isinstance(context, ListenerContext)
        )

    @worker.execute()
    def rpc_worker(context: ListenerContext) -> None:
        rpc_worker_listener_context_received.set_result(
            isinstance(context, ListenerContext)
        )

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_listener_context_parameter_test_queue"
    ).publish_as_arguments()

    assert await consumer_listener_context_received

    await rabbitmq_connector.rpc_client(
        "rpc_worker_listener_context_parameter_test_queue", timeout=5
    ).call_with_arguments()

    assert await rpc_worker_listener_context_received


@mark.asyncio
async def test_rabbitmq_listener_flow_control(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consumer_flow_control_set = loop.create_future()
    rpc_worker_flow_control_set = loop.create_future()
    consumer = Consumer("consumer_flow_control_test_queue")
    worker = RpcWorker("rpc_worker_flow_control_test_queue")

    @consumer.consume()
    async def message_consumer(context: ListenerContext) -> None:
        if not consumer_flow_control_set.done():
            await context.flow_control.request(10)
            consumer_flow_control_set.set_result(True)

    @worker.execute()
    async def rpc_worker(context: ListenerContext) -> None:
        if not rpc_worker_flow_control_set.done():
            await context.flow_control.request(10)
            rpc_worker_flow_control_set.set_result(True)

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()

    publisher = rabbitmq_connector.publisher("consumer_flow_control_test_queue")
    rpc_client = rabbitmq_connector.rpc_client(
        "rpc_worker_flow_control_test_queue", timeout=5
    )

    await publisher.publish_as_arguments()

    assert await consumer_flow_control_set

    await rpc_client.call_with_arguments()

    assert await rpc_worker_flow_control_set


@mark.asyncio
async def test_rabbitmq_rpc_exception_handler_reply(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    worker = RpcWorker("rpc_exception_handler_reply_test_queue")

    @worker.execute()
    async def rpc_worker() -> None:
        raise ValueError("value_error")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    class ValueErrorHandler(AbstractRabbitMqExceptionHandler):
        @property
        def exception(self) -> type[Exception]:
            return cast(type[Exception], ValueError)

        async def __call__(
            self, context: ListenerContext, error: Exception
        ) -> None:
            assert context.rpc_reply is not None

            await context.rpc_reply.reply(str(error))

    rabbitmq_connector.set_exception_handlers(ValueErrorHandler)
    rabbitmq_connector.include_listener(worker)
    await rabbitmq_connector.connect()

    result = await rabbitmq_connector.rpc_client(
        "rpc_exception_handler_reply_test_queue", timeout=0.1
    ).call()

    assert result == "value_error"


@mark.asyncio
async def test_rabbitmq_class_based_listener(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consume_class_future = loop.create_future()

    @consumer("consumer_class_based_listener_queue")
    class TestConsumer(ListenerBase):
        @consume()
        def consume_test_message(self) -> None:
            consume_class_future.set_result("recieved")

    @rpc_worker("rpc_worker_class_based_listener_queue")
    class TestRpcWorker(ListenerBase):
        @execute()
        def reply_message(self) -> str:
            return "recieved"

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(TestConsumer)
    rabbitmq_connector.include_listener(TestRpcWorker)
    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_class_based_listener_queue"
    ).publish_as_arguments()

    assert await consume_class_future == "recieved"
    assert (
        await rabbitmq_connector.rpc_client(
            "rpc_worker_class_based_listener_queue", timeout=0.1
        ).call()
        == "recieved"
    )


@mark.asyncio
async def test_rabbitmq_class_based_listener_dependency(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consume_class_future = loop.create_future()

    class TestService:
        def __init__(self) -> None:
            self._value = 0

        @property
        def value(self) -> int:
            return self._value

        @value.setter
        def value(self, value: int) -> None:
            self._value = value

    @consumer("consumer_class_based_listener_dependency_queue")
    class TestConsumer(ListenerBase):
        def __init__(self, test_service: TestService) -> None:
            self._test_service = test_service

        @consume()
        def consume_test_message(self) -> None:
            self._test_service.value = 10
            consume_class_future.set_result("recieved")

    container = Container()
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        container=container,
        remote_logger=remote_logger,
    )
    test_service = TestService()

    rabbitmq_connector.include_listener(TestConsumer)
    container.register(TestService, instance=test_service)

    await rabbitmq_connector.connect()
    await rabbitmq_connector.publisher(
        "consumer_class_based_listener_dependency_queue"
    ).publish_as_arguments()

    assert await consume_class_future == "recieved"
    assert test_service.value == 10


@mark.asyncio
async def test_rabbitmq_service(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        async def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            self._connection = connection
            self._channel_pool = channel_pool

            test_rabbitmq_service_future: Future[None] = (
                self.loop.create_future()
            )

            test_rabbitmq_service_future.set_result(None)

            return test_rabbitmq_service_future

        @property
        def connection(self) -> AsyncioConnection:
            return self._connection

        @property
        def channel_pool(self) -> ChannelPool:
            return self._channel_pool

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    test_rabbitmq_service = TestRabbitmqService()

    rabbitmq_connector.include_service(test_rabbitmq_service)
    await rabbitmq_connector.connect()

    assert test_rabbitmq_service.connection is not None
    assert test_rabbitmq_service.channel_pool is not None


@mark.asyncio
async def test_rabbitmq_uninitialized_service(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestSeviceDependency:
        pass

    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        def __init__(self, sevice_dependency: TestSeviceDependency) -> None:
            self._sevice_dependency = sevice_dependency

        def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            self._connection = connection
            self._channel_pool = channel_pool

            test_rabbitmq_service_future: Future[None] = (
                self.loop.create_future()
            )

            test_rabbitmq_service_future.set_result(None)

            return test_rabbitmq_service_future

        @property
        def sevice_dependency(self) -> TestSeviceDependency:
            return self._sevice_dependency

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    sevice_dependency = TestSeviceDependency()

    rabbitmq_connector.container.register(
        service=TestSeviceDependency, instance=sevice_dependency
    )
    rabbitmq_connector.include_service(TestRabbitmqService)
    await rabbitmq_connector.connect()

    test_rabbitmq_service = rabbitmq_connector.container.resolve(
        AbstractRabbitMQService
    )

    assert isinstance(test_rabbitmq_service, TestRabbitmqService)
    assert test_rabbitmq_service.sevice_dependency == sevice_dependency


@mark.asyncio
async def test_rabbitmq_service_resolusion_error(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        def __init__(self) -> None:
            raise ValueError("test rabbitmq service value error")

        def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            self._connection = connection
            self._channel_pool = channel_pool

            test_rabbitmq_service_future: Future[None] = (
                self.loop.create_future()
            )

            test_rabbitmq_service_future.set_result(None)

            return test_rabbitmq_service_future

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_service(TestRabbitmqService)

    with raises(ValueError) as exception_info:
        await rabbitmq_connector.connect()

    assert str(exception_info.value) == "test rabbitmq service value error"


@mark.asyncio
async def test_rabbitmq_service_initialization_method_error(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            self._connection = connection
            self._channel_pool = channel_pool

            raise ValueError("method value error")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_service(TestRabbitmqService)

    with raises(ValueError) as exception_info:
        await rabbitmq_connector.connect()

    assert str(exception_info.value) == "method value error"


@mark.asyncio
async def test_rabbitmq_service_initialization_future_error(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            self._connection = connection
            self._channel_pool = channel_pool

            test_rabbitmq_service_future: Future[None] = (
                self.loop.create_future()
            )

            test_rabbitmq_service_future.set_exception(
                ValueError("future value error")
            )

            return test_rabbitmq_service_future

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_service(TestRabbitmqService)

    with raises(ValueError) as exception_info:
        await rabbitmq_connector.connect()

    assert str(exception_info.value) == "future value error"


@mark.asyncio
async def test_rabbitmq_service_error_reconnection(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    loop = get_running_loop()
    consume_future = loop.create_future()
    consumer = Consumer("service_error_reconnection_test_queue")
    connected = False

    class TestRabbitmqService(AbstractRabbitMQService, AsyncEventLoopMixin):
        def initialize(
            self, connection: AsyncioConnection, channel_pool: ChannelPool
        ) -> Future[None]:
            nonlocal connected

            self._connection = connection
            self._channel_pool = channel_pool

            test_rabbitmq_service_future: Future[None] = (
                self.loop.create_future()
            )

            if connected:
                test_rabbitmq_service_future.set_exception(
                    ValueError("future value error")
                )
            else:
                test_rabbitmq_service_future.set_result(None)
                connected = True

            return test_rabbitmq_service_future

    @consumer.consume()
    def payload_consumer(payload: str) -> None:
        consume_future.set_result("test payload")

    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        reconnect_delay=0.1,
        reconnect_delay_jitter=(0.0, 0.1),
        remote_logger=remote_logger,
    )

    rabbitmq_connector.include_listener(consumer)
    rabbitmq_connector.include_service(TestRabbitmqService)
    await rabbitmq_connector.connect()

    rabbitmq.exec(
        f'rabbitmqctl close_all_user_connections {rabbitmq.username} "testing reason"'
    )
    rabbitmq.exec(
        'rabbitmqadmin publish exchange=amq.default routing_key=service_error_reconnection_test_queue payload="test payload"'
    )

    assert await consume_future == "test payload"


@mark.asyncio
async def test_rabbitmq_base_channel_open_error(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    class TestChannel(BaseChannel):
        def __init__(self, connection: AsyncioConnection) -> None:
            super().__init__(connection=connection)

        def _hook_on_channel_opened(self) -> None:
            raise ValueError("test channel value error")

    channel = TestChannel(connection=rabbitmq_connector.connection)

    with raises(ValueError) as exception_info:
        await channel.open()

    assert str(exception_info.value) == "test channel value error"


@mark.asyncio
async def test_rabbitmq_base_channel_unopened(
    rabbitmq: RabbitMqContainer, remote_logger: BaseRemoteLogSender
) -> None:
    rabbitmq_connector = RabbitMqManager(
        parameters=rabbitmq.get_connection_params(),
        remote_logger=remote_logger,
    )

    await rabbitmq_connector.connect()

    class TestChannel(BaseChannel):
        def __init__(self, connection: AsyncioConnection) -> None:
            super().__init__(connection=connection)

        def _hook_on_channel_opened(self) -> None:
            raise ValueError("test channel value error")

    channel = TestChannel(connection=rabbitmq_connector.connection)

    with raises(RuntimeError) as exception_info:
        with channel as _:
            pass

    assert str(exception_info.value) == "underlying channel not opened yet"

    with raises(RuntimeError) as exception_info:
        _ = channel.channel

    assert str(exception_info.value) == "underlying channel not opened yet"
