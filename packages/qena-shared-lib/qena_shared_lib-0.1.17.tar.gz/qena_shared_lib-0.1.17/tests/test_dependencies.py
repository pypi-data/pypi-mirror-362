from inspect import signature
from typing import Annotated, Any

from fastapi import FastAPI
from pytest import raises

from qena_shared_lib.application import Builder
from qena_shared_lib.dependencies import Container
from qena_shared_lib.dependencies.http import (
    add_service,
    get_container,
    get_service,
)
from qena_shared_lib.dependencies.miscellaneous import (
    DependsOn,
    validate_annotation,
)


def test_none_existing_container() -> None:
    app = FastAPI()

    with raises(RuntimeError) as exception_info:
        _ = get_container(app)

    assert (
        str(exception_info.value)
        == "application does include container, possibly not created with builder"
    )


def test_none_container() -> None:
    class NoneContainer:
        pass

    app = FastAPI()

    app.state.container = NoneContainer()

    with raises(TypeError) as exception_info:
        _ = get_container(app)

    assert (
        str(exception_info.value) == "container is not type of `punq.Container`"
    )


def test_container() -> None:
    app = Builder().build()

    container = get_container(app)

    assert isinstance(container, Container)


def test_container_service() -> None:
    class MockService:
        pass

    app = Builder().build()

    add_service(app=app, service=MockService)

    service = get_service(app=app, service_key=MockService)

    assert isinstance(service, MockService)


def test_validate_function_with_no_annotation() -> None:
    def function_with_no_annotation(arg_one: Any) -> None:
        pass

    assert all(
        validate_annotation(parameter) is None
        for parameter in signature(
            function_with_no_annotation
        ).parameters.values()
    )


def test_validate_function_with_none_annotated_annotation() -> None:
    def function_with_none_annotated_annotation(arg_one: int) -> None:
        pass

    assert all(
        validate_annotation(parameter) is None
        for parameter in signature(
            function_with_none_annotated_annotation
        ).parameters.values()
    )


def test_validate_function_with_more_than_two_annotated_arg_annotation() -> (
    None
):
    def function_with_more_than_two_annotated_arg_annotation(
        arg_one: Annotated[int, int, int],
    ) -> None:
        pass

    assert all(
        validate_annotation(parameter) is None
        for parameter in signature(
            function_with_more_than_two_annotated_arg_annotation
        ).parameters.values()
    )


def test_validate_function_with_none_depends_on_annotated_arg_annotation() -> (
    None
):
    def function_with_none_depends_on_annotated_arg_annotation(
        arg_one: Annotated[int, str],
    ) -> None:
        pass

    assert all(
        validate_annotation(parameter) is None
        for parameter in signature(
            function_with_none_depends_on_annotated_arg_annotation
        ).parameters.values()
    )


def test_validate_function_with_depends_on_annotated_arg_annotation() -> None:
    def function_with_depends_on_annotated_arg_annotation(
        arg_one: Annotated[int, DependsOn(int)],
    ) -> None:
        pass

    assert all(
        validate_annotation(parameter) is int
        for parameter in signature(
            function_with_depends_on_annotated_arg_annotation
        ).parameters.values()
    )
