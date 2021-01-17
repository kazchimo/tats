from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from returns.primitives.hkt import Kind1

from tats.Functor import Functor
from tats.data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class FunctorSyntax(Generic[F, A], ABC):

  @property
  @abstractmethod
  def _functor_instance(self) -> Type[Functor[F]]:
    ...

  @property
  @abstractmethod
  def _self(self) -> Kind1[F, A]:
    ...

  def map(self, f: Func1[A, B]) -> Kind1[F, B]:
    return self._functor_instance.map(self._self, f)
