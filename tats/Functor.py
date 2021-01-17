from abc import abstractmethod, ABC
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


class FunctorSyntax(Generic[URI, A], ABC):

  @property
  @abstractmethod
  def _functor_instance(self) -> Type[Functor[URI]]:
    ...

  @property
  @abstractmethod
  def _self(self) -> Kind1[URI, A]:
    ...

  def map(self, f: Func1[A, B]) -> Kind1[URI, B]:
    return self._functor_instance.map(self._self, f)
