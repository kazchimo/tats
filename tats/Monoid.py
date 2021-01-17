from abc import ABC, abstractmethod
from typing import TypeVar

from .Semigroup import Semigroup

T = TypeVar("T")


class Monoid(Semigroup[T], ABC):

  @property
  @abstractmethod
  def empty(self) -> T:
    ...
