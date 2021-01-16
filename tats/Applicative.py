from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Apply import Apply, apply_syntax
from .Functor import B, functor_syntax
from .Op import UnOp

URI = TypeVar("URI", bound=str)
A = TypeVar("A")


class Applicative(Generic[URI], Apply[URI]):

  @classmethod
  def map(cls, fa: Kind1[URI, A], f: UnOp[A, B]) -> Kind1[URI, B]:
    return cls.ap(cls.pure(f), fa)

  @staticmethod
  @abstractmethod
  def pure(a: A) -> Kind1[URI, A]:
    ...


def applicative_syntax(instance: Type[Applicative[URI]]):

  def _add_syntax(c):
    apply_syntax(instance)(c)
    return c

  return _add_syntax
