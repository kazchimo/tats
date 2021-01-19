from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.Functor import Functor
from tats.SelfIs import SelfIs
from tats.data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasFunctorInstance(Generic[F]):
  @staticmethod
  @abstractmethod
  def _functor_instance() -> Functor[F]:
    ...


class FunctorSyntax(Generic[F], SelfIs[F], HasFunctorInstance[F], ABC):
  def map(self, f: Func1[A, B]) -> Kind1[F, B]:
    return self._functor_instance().map(self._self, f)
