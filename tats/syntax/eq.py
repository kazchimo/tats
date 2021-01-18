from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from tats.Eq import Eq
from tats.SelfIs import SelfIs

T = TypeVar("T")


class HasEqInstance(Generic[T], ABC):

  @property
  @abstractmethod
  def _eq_instance(self) -> Eq[T]:
    ...


class EqSyntax(Generic[T], SelfIs[T], HasEqInstance[T]):

  def eqv(self, r: T) -> bool:
    return self._eq_instance.eqv(self._self, r)

  def neqv(self, r: T) -> bool:
    return self._eq_instance.neqv(self._self, r)


class DeriveEq(EqSyntax[T], ABC):

  @property
  def _eq_instance(self) -> Eq[T]:
    return Eq(lambda a, b: a == b)
