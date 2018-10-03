from abc import abstractmethod
from typing import Generic, TypeVar

L = TypeVar('L')
R = TypeVar('R')


class Either(Generic[L, R]):

    @property
    @abstractmethod
    def is_left(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_right(self) -> bool:
        pass

    @property
    @abstractmethod
    def value(self) -> L or R:
        pass


class Left(Either):
    def __init__(self, v):
        self.v = v

    @property
    def is_left(self) -> bool:
        return True

    @property
    def is_right(self) -> bool:
        return False

    @property
    def value(self) -> L:
        return self.v


class Right(Either):
    def __init__(self, v):
        self.v = v

    @property
    def is_left(self) -> bool:
        return False

    @property
    def is_right(self) -> bool:
        return True

    @property
    def value(self) -> R:
        return self.v
