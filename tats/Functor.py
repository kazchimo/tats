from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from .data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Functor(Generic[F]):

  @staticmethod
  @abstractmethod
  def map(fa: Kind1[F, A], f: Func1[A, B]) -> Kind1[F, B]:
    ...
