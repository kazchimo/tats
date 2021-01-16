from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Optional, Any, Literal

from returns.primitives.hkt import SupportsKind1, Kind1

from .Apply import Apply, apply_syntax
from .Op import UnOp

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class OptionInstance(Apply[URI]):

  @staticmethod
  def map(fa: Kind1[URI, A], f: UnOp[A, B]) -> Kind1[URI, B]:
    return OptionInstance.ap(Some(f), fa)

  @staticmethod
  def ap(ff: Kind1[URI, UnOp[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    if ff.is_empty():
      return Nothing()
    else:
      if fa.is_empty():
        return Nothing()
      else:
        return Some(ff.a(fa.a))


@apply_syntax(OptionInstance)
class Option(SupportsKind1[URI, A]):

  @abstractmethod
  def is_empty(self) -> bool:
    ...

  @abstractmethod
  def non_empty(self) -> bool:
    ...

  @staticmethod
  def pure(a: Optional[A]) -> "Option[A]":
    return Some(a) if a is not None else Nothing()


@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False

  def non_empty(self) -> bool:
    return True


@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True

  def non_empty(self) -> bool:
    return False
