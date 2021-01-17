from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Semigroup(Generic[T]):

  @staticmethod
  @abstractmethod
  def _cmb(a: T, b: T) -> T:
    ...

  def combine(self, a: T, b: T) -> T:
    return self._cmb(a, b)


class Kind1Semigroup(Generic[S, T]):

  @staticmethod
  @abstractmethod
  def _cmb(tsemi: Semigroup[T], a: S, b: S) -> S:
    ...

  def combine(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    return self._cmb(tsemi, a, b)
