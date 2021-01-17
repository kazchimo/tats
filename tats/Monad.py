from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from .Applicative import Applicative
from .FlatMap import FlatMap
from .data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Monad(Generic[F], FlatMap[F], Applicative[F]):

  @classmethod
  def map(cls, fa: Kind1[F, A], f: Func1[A, B]) -> Kind1[F, B]:
    return cls.flat_map(fa, lambda x: cls.pure(f(x)))
