from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from tats.SelfIs import SelfIs
from tats.Semigroup import Semigroup, Kind1Semigroup

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class SemigroupSyntax(Generic[T], SelfIs[T]):
  def __add__(self, other: T):
    return self.combine(other)

  def combine(self, other: T) -> T:
    return self._semigroup_instance.combine(self._self, other)

  @property
  @abstractmethod
  def _semigroup_instance(self) -> Semigroup[T]:
    ...


class Kind1SemigroupSyntax(Generic[S, T], SelfIs[S]):
  def combine(self, tsemi: Semigroup[T], other: S) -> S:
    return self._semigroup_instance().combine(tsemi, self._self, other)

  @abstractmethod
  def _semigroup_instance(self) -> Kind1Semigroup[S, T]:
    ...
