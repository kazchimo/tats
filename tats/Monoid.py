from abc import ABC, abstractmethod
from typing import TypeVar

from returns.primitives.hkt import Kind1

from .Semigroup import Semigroup, Kind1Semigroup

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Monoid(Semigroup[T], ABC):
  @staticmethod
  @abstractmethod
  def empty() -> T:
    ...

  @classmethod
  def reverse(cls) -> "Monoid[T]":
    class _Monoid(Monoid[T]):
      @staticmethod
      def combine(a: T, b: T) -> T:
        return cls.combine(b, a)

      @staticmethod
      def empty() -> T:
        return cls.empty()

      @classmethod
      def reverse(_self) -> "Monoid[T]":
        return cls()

    return _Monoid()


class Kind1Monoid(Kind1Semigroup[S, T]):
  @abstractmethod
  def empty(self) -> S:
    ...
