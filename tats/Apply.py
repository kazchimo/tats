from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Functor import Functor, FunctorSyntax
from .Op import Func1

URI = TypeVar("URI")
A = TypeVar("A")
B = TypeVar("B")


class Apply(Generic[URI], Functor[URI]):

  @staticmethod
  @abstractmethod
  def ap(ff: Kind1[URI, Func1[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    ...

  @classmethod
  def product_r(cls, fa: Kind1[URI, A], fb: Kind1[URI, B]) -> Kind1[URI, B]:
    return cls.ap(cls.map(fa, lambda _: lambda b: b), fb)

  @classmethod
  def product_l(cls, fa: Kind1[URI, A], fb: Kind1[URI, B]) -> Kind1[URI, A]:
    return cls.ap(cls.map(fa, lambda a: lambda _: a), fb)


class ApplySyntax(Generic[URI, A], FunctorSyntax[URI, A]):

  def product_r(self, fb: Kind1[URI, B]) -> Kind1[URI, B]:
    return self._apply_instance.product_r(self._self, fb)

  def product_l(self, fb: Kind1[URI, B]) -> Kind1[URI, A]:
    return self._apply_instance.product_l(self._self, fb)

  @property
  @abstractmethod
  def _apply_instance(self) -> Type[Apply[URI]]:
    ...

  @property
  def _functor_instance(self) -> Type[Functor[URI]]:
    return self._apply_instance
