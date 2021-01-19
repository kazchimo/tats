from abc import abstractmethod
from typing import Generic, TypeVar, Tuple

from returns.primitives.hkt import Kind1

from .Functor import Functor
from .data.Function import Func1, Func2

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class Apply(Generic[F], Functor[F]):
  @staticmethod
  @abstractmethod
  def ap(ff: Kind1[F, Func1[A, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
    ...

  @classmethod
  def product_r(cls, fa: Kind1[F, A], fb: Kind1[F, B]) -> Kind1[F, B]:
    return cls.ap(cls.map(fa, lambda _: lambda b: b), fb)

  @classmethod
  def product_l(cls, fa: Kind1[F, A], fb: Kind1[F, B]) -> Kind1[F, A]:
    return cls.ap(cls.map(fa, lambda a: lambda _: a), fb)

  @classmethod
  def map2(cls, fa: Kind1[F, A], fb: Kind1[F, B], f: Func2[A, B, C]) -> Kind1[F, C]:
    return cls.map(cls.product(fa, fb), lambda a: f(a[0], a[1]))

  @classmethod
  def product(cls, fa: Kind1[F, A], fb: Kind1[F, B]) -> Kind1[F, Tuple[A, B]]:
    return cls.ap(cls.map(fa, lambda a: lambda b: (a, b)), fb)
