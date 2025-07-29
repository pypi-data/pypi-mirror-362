from asyncio import get_running_loop, sleep

from pytest import mark

from qena_shared_lib.background import Background, BackgroundTask
from qena_shared_lib.dependencies import Container, Scope
from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    RemoteLogRecord,
    SenderResponse,
)


class MockRemoteLogSender(BaseRemoteLogSender):
    async def _send(self, _: RemoteLogRecord) -> SenderResponse:
        return SenderResponse(sent=True)


@mark.asyncio
async def test_same_id() -> None:
    loop = get_running_loop()
    background_task_future = loop.create_future()
    container = Container()
    remote_logger = MockRemoteLogSender(service_name="test")

    container.register(service=BaseRemoteLogSender, instance=remote_logger)
    container.register(service=Background, scope=Scope.singleton)

    background = container.resolve(Background)

    assert isinstance(background, Background)

    await remote_logger.start()
    background.start()

    async def sleep_task() -> None:
        if not background_task_future.done():
            background_task_future.set_result(None)

        await sleep(1)

    background.add_task(BackgroundTask(sleep_task), "task1")
    background.add_task(BackgroundTask(sleep_task), "task1")

    await background_task_future

    assert background.is_alive("task1")
    assert background.count() == 1

    background.stop()
    await remote_logger.stop()


@mark.asyncio
async def test_two_tasks() -> None:
    loop = get_running_loop()
    background_task_future = loop.create_future()
    container = Container()
    remote_logger = MockRemoteLogSender(service_name="test")

    container.register(service=BaseRemoteLogSender, instance=remote_logger)
    container.register(service=Background, scope=Scope.singleton)

    background = container.resolve(Background)

    assert isinstance(background, Background)

    await remote_logger.start()
    background.start()

    async def sleep_task() -> None:
        if not background_task_future.done():
            background_task_future.set_result(None)

        await sleep(1)

    background.add_task(BackgroundTask(sleep_task), "task1")
    background.add_task(BackgroundTask(sleep_task), "task2")

    await background_task_future

    assert background.count() == 2
    assert background.is_alive("task1")
    assert background.is_alive("task2")

    background.stop()
    await remote_logger.stop()
