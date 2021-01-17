from abc import ABC, abstractmethod
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


class EqSyntax(Generic[T]):

  @property
  @abstractmethod
  def _eq_instance(self) -> Eq[T]:
    ...

  @property
  @abstractmethod
  def _self(self) -> T:
    ...

  def eqv(self, r: T) -> bool:
    return self._eq_instance.eqv(self._self, r)

  def neqv(self, r: T) -> bool:
    return self._eq_instance.neqv(self._self, r)


class DeriveEq(EqSyntax[T], ABC):

  @property
  def _eq_instance(self) -> Eq[T]:
    return Eq(lambda a, b: a == b)
