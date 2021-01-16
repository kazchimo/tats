from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Functor import Functor, functor_syntax
from .Op import UnOp

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Apply(Generic[URI], Functor[URI]):

  @staticmethod
  @abstractmethod
  def ap(ff: Kind1[URI, UnOp[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    ...


def apply_syntax(instance: Type[Apply[URI]]):

  def _add_syntax(c):

    def _product_r(self, fb):

      return instance.ap(instance.map(self, lambda _: lambda b: b), fb)

    setattr(c, "product_r", _product_r)
    functor_syntax(instance)(c)
    return c

  return _add_syntax
