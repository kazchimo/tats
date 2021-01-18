from abc import abstractmethod
from typing import TypeVar

from returns.primitives.hkt import Kind1

from tats.Monoid import Monoid, Kind1Monoid
from tats.SelfIs import SelfIs
from tats.Semigroup import Semigroup, Kind1Semigroup
from tats.syntax.eq import HasEqInstance
from tats.syntax.semigroup import SemigroupSyntax, Kind1SemigroupSyntax

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class MonoidSyntax(SemigroupSyntax[T], SelfIs[T], HasEqInstance[T]):

  @property
  @abstractmethod
  def _monoid_instance(self) -> Monoid[T]:
    ...

  @property
  def _semigroup_instance(self) -> Semigroup[T]:
    return self._monoid_instance

  @property
  def is_empty(self) -> bool:
    return self._eq_instance.eqv(self._self, self._monoid_instance.empty)


class Kind1MonoidSyntax(Kind1SemigroupSyntax[S, T], HasEqInstance[S]):

  def _semigroup_instance(self) -> Kind1Semigroup[S, T]:
    return self._monoid_instance

  @property
  @abstractmethod
  def _monoid_instance(self) -> Kind1Monoid[S, T]:
    ...

  def is_empty(self) -> bool:
    return self._eq_instance.eqv(self._self, self._monoid_instance.empty())
