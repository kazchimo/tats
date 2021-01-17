from abc import abstractmethod
from typing import TypeVar, Generic, Type

from returns.primitives.hkt import Kind1

from .Op import Func1

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class Functor(Generic[URI]):

  @staticmethod
  @abstractmethod
  def map(fa: Kind1[URI, A], f: Func1[A, B]) -> Kind1[URI, B]:
    ...


def functor_syntax(instance: Type[Functor[URI]]):

  def _add_syntax(c: C):

    def _map(self, f: Func1[A, B]):
      return instance.map(self, f)

    setattr(c, "map", _map)
    return c

  return _add_syntax
