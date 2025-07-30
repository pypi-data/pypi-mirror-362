from datetime import datetime, timedelta
from typing import Annotated, Any

from pytest import raises

from qena_shared_lib.dependencies.miscellaneous import DependsOn
from qena_shared_lib.remotelogging import BaseRemoteLogSender
from qena_shared_lib.scheduler import (
    ScheduleManager,
    Scheduler,
    SchedulerBase,
    schedule,
    scheduler,
)


def test_schedueler_scheduled_task(remote_logger: BaseRemoteLogSender) -> None:
    scheduler = Scheduler()

    @scheduler.schedule("* * * * *")
    def schedule_for_every_minute() -> None:
        pass

    schedule_manager = ScheduleManager(remote_logger=remote_logger)

    schedule_manager.include_scheduler(scheduler)

    scheduler_start = datetime.now()
    scheduler_end = datetime.now() + timedelta(
        seconds=schedule_manager.next_run_in
    )

    assert (scheduler_end - scheduler_start).seconds <= 60


def test_schedueler_class_based_scheduled_task(
    remote_logger: BaseRemoteLogSender,
) -> None:
    @scheduler()
    class TestScheduler(SchedulerBase):
        @schedule("* * * * *")
        def schedule_for_every_minute(self) -> None:
            pass

    schedule_manager = ScheduleManager(remote_logger=remote_logger)

    schedule_manager.include_scheduler(TestScheduler)
    schedule_manager.use_schedulers()

    scheduler_start = datetime.now()
    scheduler_end = datetime.now() + timedelta(
        seconds=schedule_manager.next_run_in
    )

    assert schedule_manager.scheduled_task_count == 1
    assert (scheduler_end - scheduler_start).seconds <= 60


def test_schedueler_scheduled_task_wrong_parameter() -> None:
    scheduler = Scheduler()

    with raises(TypeError) as exception_info:

        @scheduler.schedule("* * * * *")
        def schedule_for_every_minute(arg_one: dict[str, Any]) -> None:
            pass

    assert (
        str(exception_info.value)
        == "scheduler parament annotation for `arg_one` not valid, expected `Annotated[type, DependsOn(type)]`"
    )


def test_schedueler_class_based_scheduled_task_wrong_parameter(
    remote_logger: BaseRemoteLogSender,
) -> None:
    @scheduler()
    class TestScheduler(SchedulerBase):
        @schedule("* * * * *")
        def schedule_for_every_minute(self, arg_one: dict[str, Any]) -> None:
            pass

    schedule_manager = ScheduleManager(remote_logger=remote_logger)

    schedule_manager.include_scheduler(TestScheduler)

    with raises(TypeError) as exception_info:
        schedule_manager.use_schedulers()

    assert (
        str(exception_info.value)
        == "scheduler parament annotation for `arg_one` not valid, expected `Annotated[type, DependsOn(type)]`"
    )


def test_scheduler_scheduled_tasks_parameters() -> None:
    scheduler = Scheduler()

    @scheduler.schedule("* * * * *")
    def schedule_for_every_minute(
        arg_one: Annotated[dict[str, Any], DependsOn(dict[str, Any])],
        arg_two: Annotated[set[Any], DependsOn(set[Any])],
    ) -> None:
        pass

    *_, scheduled_task = scheduler.scheduled_tasks

    assert scheduled_task.parameters == {
        "arg_one": dict[str, Any],
        "arg_two": set[Any],
    }
