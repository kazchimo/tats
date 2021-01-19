from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Semigroup(Generic[T]):
  @staticmethod
  @abstractmethod
  def combine(a: T, b: T) -> T:
    ...

  @classmethod
  def reverse(cls) -> "Semigroup[T]":
    class _Semigroup(Semigroup[T]):
      @staticmethod
      def combine(a: T, b: T) -> T:
        return cls.combine(b, a)

      @classmethod
      def reverse(_cls) -> "Semigroup[T]":
        return cls()

    return _Semigroup()


class Kind1Semigroup(Generic[S, T]):
  @abstractmethod
  def _cmb(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    ...

  def combine(self, tsemi: Semigroup[T], a: S, b: S) -> S:
    return self._cmb(tsemi, a, b)
