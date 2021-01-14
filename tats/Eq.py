from abc import ABC, abstractmethod
from types import new_class
from typing import Generic, TypeVar, Dict, Any, Type

from .BiOp import BiOp

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
  def instance(name: str,  eqv: BiOp[_T, bool]) -> "Type[Eq[_T]]":
    def upd(d: Dict[str, Any]):
      d.update({"eqv": eqv})
    return new_class(name, (Eq[_T], ), exec_body=upd)

IntEq: Type[Eq[int]] = Eq.instance("IntEq", lambda a, b: a == b)
