from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Literal

from returns.primitives.hkt import SupportsKind1, Kind1

from .Eq import derive_eq
from .Applicative import Applicative, applicative_syntax
from .Op import UnOp

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class OptionInstance(Applicative[URI]):

  @staticmethod
  def pure(a: A) -> Kind1[URI, A]:
    return Some(a)

  @staticmethod
  def ap(ff: Kind1[URI, UnOp[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    if ff.is_empty():
      return Nothing()
    else:
      if fa.is_empty():
        return Nothing()
      else:
        return Some(ff.a(fa.a))


@derive_eq
@applicative_syntax(OptionInstance)
class Option(SupportsKind1[URI, A]):

  @abstractmethod
  def is_empty(self) -> bool:
    ...

  def non_empty(self) -> bool:
    return not self.is_empty()

  def or_else(self, alt: "Option[A]") -> "Option[A]":
    return self if self.non_empty() else alt


@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False


@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True
