from dataclasses import dataclass
from typing import Generic, TypeVar

from .Op import BiOp

T = TypeVar("T")

@dataclass(frozen=True)
class Eq(Generic[T]):
  _eqv: BiOp[T, bool]

  def eqv(self, l: T, r: T) -> bool:
    return self._eqv(l, r)

  def neqv(self, l: T, r: T) -> bool:
    return not self.eqv(l, r)

