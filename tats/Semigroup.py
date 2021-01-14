from abc import abstractmethod, ABC
from typing import TypeVar, Generic

_T = TypeVar("_T")

class Semigroup(Generic[_T], ABC):
  @staticmethod
  @abstractmethod
  def combine(l: _T, r: _T) -> _T:
    ...


