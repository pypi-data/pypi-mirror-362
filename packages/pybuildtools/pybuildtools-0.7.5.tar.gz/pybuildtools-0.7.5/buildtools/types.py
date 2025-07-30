

from abc import abstractmethod
import os
from typing import Container, Iterable, Iterator, Protocol, TypeVar, Union, runtime_checkable

StrOrPath = os.PathLike

T = TypeVar('T')


@runtime_checkable
class SupportsContains(Protocol[T]):
    """An ABC with one abstract method __contains__."""
    __slots__ = ()

    @abstractmethod
    def __contains__(self, other: T) -> bool:
        pass


@runtime_checkable
class SupportsIter(Protocol[T]):
    """An ABC with one abstract method __iter__."""
    __slots__ = ()

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass


# SupportsIn = Union[SupportsContains[T],SupportsIter[T]]
SupportsIn = Union[Container[T], Iterable[T]]
