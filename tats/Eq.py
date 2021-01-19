from abc import abstractmethod
from typing import Generic, TypeVar

from .data.Function import Func1, BiOp

T = TypeVar("T")
S = TypeVar("S")


class Eq(Generic[T]):
  @staticmethod
  @abstractmethod
  def eqv(l: T, r: T) -> bool:
    ...

  @classmethod
  def neqv(cls, l: T, r: T) -> bool:
    return not cls.eqv(l, r)

  def contramap(self, f: Func1[S, T]) -> "Eq[S]":
    return Eq.instance(lambda l, r: self.eqv(f(l), f(r)))

  def and_(self, other: "Eq[T]") -> "Eq[T]":
    return Eq.instance(lambda l, r: self.eqv(l, r) and other.eqv(l, r))

  @staticmethod
  def instance(f: BiOp[T, bool]) -> "Eq[T]":
    class _Eq(Eq[S]):
      @staticmethod
      def eqv(l: S, r: S) -> bool:
        return f(l, r)

    return _Eq()
