from abc import ABC, abstractmethod
from types import new_class
from typing import Generic, TypeVar, Dict, Callable, Any, Type

_T = TypeVar("_T")

class Eq(Generic[_T], ABC):
  @staticmethod
  @abstractmethod
  def eqv(l: _T, r: _T) -> bool:
    ...

  @classmethod
  def neqv(cls, l: _T, r: _T) -> bool:
    return not cls.eqv(l, r)

  @staticmethod
  def instance(name: str, eqv: Callable[[_T, _T], bool]) -> "Type[Eq[_T]]":
    def upd(d: Dict[str, Any]):
      d.update({"eqv": eqv})
    return new_class(name, (Eq[_T], ), exec_body=upd)
