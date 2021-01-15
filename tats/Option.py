from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Any

_T = TypeVar("_T", covariant=True)

class Option(Generic[_T], ABC):
  @abstractmethod
  def is_empty(self) -> bool:
    ...

  @staticmethod
  def pure(a: Optional[_T]) -> "Option[_T]":
    return Some(a) if a is not None else Nothing()

@dataclass(frozen=True)
class Some(Option[_T]):
  a: _T

  def is_empty(self) -> bool:
    return False

@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True
