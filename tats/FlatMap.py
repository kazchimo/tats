from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from tats.syntax.apply import ApplySyntax
from .data.Function import Func1
from .Apply import Apply

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class FlatMap(Generic[F], Apply[F]):

  @staticmethod
  @abstractmethod
  def flat_map(fa: Kind1[F, A], f: Func1[A, Kind1[F, B]]) -> Kind1[F, B]:
    ...

  @classmethod
  def flatten(cls, ffa: Kind1[F, Kind1[F, A]]) -> Kind1[F, A]:
    return cls.flat_map(ffa, lambda x: x)

  @classmethod
  def ap(cls, ff: Kind1[F, Func1[A, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
    return cls.flat_map(ff, lambda f: cls.map(fa, f))
