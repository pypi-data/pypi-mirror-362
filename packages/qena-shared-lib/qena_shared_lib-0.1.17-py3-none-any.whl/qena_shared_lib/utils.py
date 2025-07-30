from asyncio import AbstractEventLoop, get_running_loop
from typing import Generator

from pydantic import TypeAdapter

__all__ = ["AsyncEventLoopMixin", "TypeAdapterCache"]


class AsyncEventLoopMixin:
    _LOOP: AbstractEventLoop | None = None

    @property
    def loop(self) -> AbstractEventLoop:
        if self._LOOP is None:
            self._LOOP = get_running_loop()

        return self._LOOP

    def init(self) -> None:
        self._LOOP = get_running_loop()


class TypeAdapterCache:
    _cache: dict[type, TypeAdapter] = {}

    @classmethod
    def cache_annotation(cls, annotation: type) -> None:
        if annotation not in cls._cache:
            cls._cache[annotation] = TypeAdapter(annotation)

    @classmethod
    def get_type_adapter(cls, annotation: type) -> TypeAdapter:
        cls.cache_annotation(annotation)

        return cls._cache[annotation]


class YieldOnce:
    def __await__(self) -> Generator[None, None, None]:
        return (yield)


def yield_now() -> YieldOnce:
    return YieldOnce()
