from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Functor import Functor, FunctorSyntax
from .Op import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


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


class ApplySyntax(Generic[F, A], FunctorSyntax[F, A]):

  def product_r(self, fb: Kind1[F, B]) -> Kind1[F, B]:
    return self._apply_instance.product_r(self._self, fb)

  def product_l(self, fb: Kind1[F, B]) -> Kind1[F, A]:
    return self._apply_instance.product_l(self._self, fb)

  @property
  @abstractmethod
  def _apply_instance(self) -> Type[Apply[F]]:
    ...

  @property
  def _functor_instance(self) -> Type[Functor[F]]:
    return self._apply_instance
