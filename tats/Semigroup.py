from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from .SelfIs import SelfIs

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Semigroup(Generic[T]):

  @staticmethod
  @abstractmethod
  def _cmb(a: T, b: T) -> T:
    ...

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


class Kind1Semigroup(Generic[S, T]):

  @staticmethod
  @abstractmethod
  def _cmb(tsemi: Semigroup[T], a: S, b: S) -> S:
    ...

  def combine(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    return self._cmb(tsemi, a, b)


class Kind1SemigroupSyntax(Generic[S, T], SelfIs[S]):

  def combine(self, tsemi: Semigroup[T], other: S) -> S:
    return self._semigroup_instance().combine(tsemi, self._self, other)

  @abstractmethod
  def _semigroup_instance(self) -> Kind1Semigroup[S, T]:
    ...
