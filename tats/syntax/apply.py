from abc import abstractmethod
from typing import Generic, TypeVar, Tuple

from returns.primitives.hkt import Kind1

from tats.Apply import Apply
from tats.Functor import Functor
from tats.data.Function import Func2
from tats.syntax.functor import FunctorSyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class ApplySyntax(Generic[F, A], FunctorSyntax[F]):
  def product_r(self, fb: Kind1[F, B]) -> Kind1[F, B]:
    return self._apply_instance.product_r(self._self, fb)

  def product_l(self, fb: Kind1[F, B]) -> Kind1[F, A]:
    return self._apply_instance.product_l(self._self, fb)

  def map2(self, fb: Kind1[F, B], f: Func2[A, B, C]) -> Kind1[F, C]:
    return self._apply_instance.map2(self._self, fb, f)

  def product(self, fb: Kind1[F, B]) -> Kind1[F, Tuple[A, B]]:
    return self._apply_instance.product(self._self, fb)

  @property
  @abstractmethod
  def _apply_instance(self) -> Apply[F]:
    ...

  @property
  def _functor_instance(self) -> Functor[F]:
    return self._apply_instance
