from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from .Apply import Apply
from .data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Applicative(Generic[F], Apply[F]):
  @classmethod
  def map(cls, fa: Kind1[F, A], f: Func1[A, B]) -> Kind1[F, B]:
    return cls.ap(cls.pure(f), fa)

  @staticmethod
  @abstractmethod
  def pure(a: A) -> Kind1[F, A]:
    ...
