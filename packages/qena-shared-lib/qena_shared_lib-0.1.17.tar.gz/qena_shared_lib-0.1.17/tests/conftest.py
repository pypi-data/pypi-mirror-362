from typing import AsyncGenerator

from pytest_asyncio import fixture as fixture_asyncio

from qena_shared_lib.remotelogging import (
    BaseRemoteLogSender,
    RemoteLogRecord,
    SenderResponse,
)


class MockRemoteLogSender(BaseRemoteLogSender):
    async def _send(self, _: RemoteLogRecord) -> SenderResponse:
        return SenderResponse(sent=True)


@fixture_asyncio(scope="session")
async def remote_logger() -> AsyncGenerator[MockRemoteLogSender, None]:
    remote_logger = MockRemoteLogSender(service_name="test")

    await remote_logger.start()

    yield remote_logger

    await remote_logger.stop()
