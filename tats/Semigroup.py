from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from .Op import EndoBiOp
from .SelfIs import SelfIs

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


@dataclass(frozen=True)
class Semigroup(Generic[T]):
  _cmb: EndoBiOp[T]

  def combine(self, a: T, b: T) -> T:
    return self._cmb(a, b)


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
    return self._semigroup_instance(tsemi).combine(self._self, other)

  @abstractmethod
  def _semigroup_instance(self, tsemi: Semigroup[T]) -> Semigroup[S]:
    ...
