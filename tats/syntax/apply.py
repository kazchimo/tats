from abc import abstractmethod
from typing import Generic, Type, TypeVar

from returns.primitives.hkt import Kind1

from tats.Apply import Apply
from tats.Functor import Functor
from tats.syntax.functor import FunctorSyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


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
