from abc import abstractmethod, ABC
from types import new_class
from typing import TypeVar, Generic, Any, Dict, Type

from tats.Op import EndoBiOp

_T = TypeVar("_T")

class Semigroup(Generic[_T], ABC):
  @staticmethod
  @abstractmethod
  def combine(l: _T, r: _T) -> _T:
    ...

  @staticmethod
  def instance(name: str, combine: EndoBiOp[_T]) -> "Type[Semigroup[_T]]":
    def upd(d: Dict[str, Any]):
      d.update({"combine": combine})
    return new_class(name, (Semigroup[_T], ), exec_body=upd)


