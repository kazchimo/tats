from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Semigroup(Generic[T]):
  @abstractmethod
  def combine(self, a: T, b: T) -> T:
    ...

  def reverse(self) -> "Semigroup[T]":
    class _Semigroup(Semigroup[T]):
      def combine(_self, a: T, b: T) -> T:
        return self.combine(b, a)

      def reverse(_self) -> "Semigroup[T]":
        return self

    return _Semigroup()


class Kind1Semigroup(Generic[S, T]):
  @abstractmethod
  def _cmb(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    ...

  def combine(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    return self._cmb(tsemi, a, b)
