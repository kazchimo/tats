from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Op import UnOp
from .Applicative import Applicative, applicative_syntax
from .FlatMap import FlatMap

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Monad(Generic[URI], FlatMap[URI], Applicative[URI]):

  @classmethod
  def map(cls, fa: Kind1[URI, A], f: UnOp[A, B]) -> Kind1[URI, B]:
    return cls.flat_map(fa, lambda x: cls.pure(f(x)))


def monad_syntax(instance: Type[Monad[URI]]):

  def _add_syntax(c):

    def _flat_map(self, f):
      instance.flat_map(self, f)

    def _flatten(self):
      instance.flatten(self)

    setattr(c, "flat_map", _flat_map)
    setattr(c, "flatten", _flatten)

    applicative_syntax(instance)(c)
    return c

  return _add_syntax
