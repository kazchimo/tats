from abc import abstractmethod
from typing import TypeVar

from tats.Monoid import Monoid
from tats.SelfIs import SelfIs
from tats.Semigroup import Semigroup
from tats.syntax.semigroup import SemigroupSyntax

T = TypeVar("T")

class MonoidSyntax(SemigroupSyntax[T], SelfIs[T]):
    @property
    @abstractmethod
    def _monoid_instance(self) -> Monoid[T]:
        ...

    @property
    def _semigroup_instance(self) -> Semigroup[T]:
        return self._monoid_instance

    @property
    @abstractmethod
    def empty(self) -> T:
        return self._monoid_instance.empty

