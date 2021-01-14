from abc import ABC, abstractmethod
from typing import TypeVar

from .Semigroup import Semigroup

_T = TypeVar("_T")

class Monoid(Semigroup[_T], ABC):
  @staticmethod
  @abstractmethod
  def empty() -> _T:
    ...

