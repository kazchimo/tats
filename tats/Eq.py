from dataclasses import dataclass
from typing import Generic, TypeVar

from .Op import BiOp, UnOp

T = TypeVar("T")
S = TypeVar("S")


@dataclass(frozen=True)
class Eq(Generic[T]):
  _eqv: BiOp[T, bool]

  def eqv(self, l: T, r: T) -> bool:
    return self._eqv(l, r)

  def neqv(self, l: T, r: T) -> bool:
    return not self.eqv(l, r)

  def contramap(self, f: UnOp[S, T]) -> "Eq[S]":
    return Eq(lambda a, b: self.eqv(f(a), f(b)))

  def and_(self, other: "Eq[T]") -> "Eq[T]":
    return Eq(lambda a, b: self.eqv(a, b) and other.eqv(a, b))


def derive_eq(c):

  def _eqv(self: T, r: T) -> bool:
    return self == r

  def _neqv(self, r):
    return not _eqv(self, r)

  setattr(c, "eqv", _eqv)
  setattr(c, "neqv", _neqv)

  return c
