from dataclasses import dataclass
from typing import Generic, TypeVar

from .data.Function import BiOp, Func1

T = TypeVar("T")
S = TypeVar("S")


@dataclass(frozen=True)
class Eq(Generic[T]):
  _eqv: BiOp[T, bool]

  def eqv(self, l: T, r: T) -> bool:
    return self._eqv(l, r)

  def neqv(self, l: T, r: T) -> bool:
    return not self.eqv(l, r)

  def contramap(self, f: Func1[S, T]) -> "Eq[S]":
    return Eq(lambda a, b: self.eqv(f(a), f(b)))

  def and_(self, other: "Eq[T]") -> "Eq[T]":
    return Eq(lambda a, b: self.eqv(a, b) and other.eqv(a, b))
