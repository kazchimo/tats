from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, NoReturn

_T = TypeVar("_T")

class Option(Generic[_T], ABC):
  @abstractmethod
  def is_empty(self) -> bool:
    ...

@dataclass(frozen=True)
class Some(Option[_T]):
  a: _T

  def is_empty(self) -> bool:
    return False

class Nothing(Option[NoReturn]):

  def is_empty(self) -> bool:
    return True
