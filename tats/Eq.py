from dataclasses import dataclass
from typing import Generic, TypeVar

from .Op import BiOp, UnOp

_T = TypeVar("_T")
_S = TypeVar("_S")

@dataclass(frozen=True)
class Eq(Generic[_T]):
  _eqv: BiOp[_T, bool]

  def eqv(self, l: _T, r: _T) -> bool:
    return self._eqv(l, r)

  def neqv(self, l: _T, r: _T) -> bool:
    return not self.eqv(l, r)

  def contramap(self, f: UnOp[_S, _T]) -> "Eq[_S]":
    return Eq(lambda a, b: self.eqv(f(a), f(b)))

  def and_(self, other: "Eq[_T]") -> "Eq[_T]":
    return Eq(lambda a, b: self.eqv(a, b) and other.eqv(a,b))


