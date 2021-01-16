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

  @classmethod
  def product_r(cls, fa: Kind1[URI, A], fb: Kind1[URI, B]) -> Kind1[URI, B]:
    return cls.ap(cls.map(fa, lambda _: lambda b: b), fb)

  @classmethod
  def product_l(cls, fa: Kind1[URI, A], fb: Kind1[URI, B]) -> Kind1[URI, A]:
    return cls.ap(cls.map(fa, lambda a: lambda _: a), fb)


def apply_syntax(instance: Type[Apply[URI]]):

  def _add_syntax(c):

    def _product_r(self, fb):
      return instance.product_r(self, fb)

    def _product_l(self, fb):
      return instance.product_l(self, fb)

    setattr(c, "product_r", _product_r)
    setattr(c, "product_l", _product_l)
    functor_syntax(instance)(c)
    return c

  return _add_syntax
