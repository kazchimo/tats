from abc import ABC, abstractmethod
from typing import TypeVar

from returns.primitives.hkt import Kind1

from .Semigroup import Semigroup, Kind1Semigroup

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Monoid(Semigroup[T], ABC):
  @property
  @abstractmethod
  def empty(self) -> T:
    ...

  def reverse(self) -> "Monoid[T]":
    class _Monoid(Monoid[T]):
      def combine(_self, a: T, b: T) -> T:
        return self.combine(b, a)

      @property
      def empty(_self) -> T:
        return self.empty

      def reverse(_self) -> "Monoid[T]":
        return self

    return _Monoid()


class Kind1Monoid(Kind1Semigroup[S, T]):
  @abstractmethod
  def empty(self) -> S:
    ...
