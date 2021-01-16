from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Optional, Any, Literal

from pampy import match, _
from returns.primitives.hkt import SupportsKind1, Kind1

from .Apply import Apply
from .Functor import Functor
from .Op import UnOp

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class Option(SupportsKind1[URI, A]):

  @abstractmethod
  def is_empty(self) -> bool:
    ...

  @staticmethod
  def pure(a: Optional[A]) -> "Option[A]":
    return Some(a) if a is not None else Nothing()


@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False


@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True


#### --- Instances ---


class OptionInstance(Functor[URI], Apply[URI]):

  @staticmethod
  def map(fa: Kind1[URI, A], f: UnOp[A, B]) -> Kind1[URI, B]:
    return match(\
      fa,
      Some(_), lambda x: Some(f(x)),
      Nothing, lambda x: Nothing())

  @staticmethod
  def ap(ff: Kind1[URI, UnOp[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    return match(\
      ff,
      Nothing, lambda _: Nothing(),
      Some(_), lambda f: OptionInstance.map(fa, f)
    )
