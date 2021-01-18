from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from tats.Eq import Eq

T = TypeVar("T")


class HasEqInstance(Generic[T], ABC):

  @property
  @abstractmethod
  def _eq_instance(self) -> Eq[T]:
    ...
