from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Literal

from returns.primitives.hkt import SupportsKind1, Kind1

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


@applicative_syntax(OptionInstance)
class Option(SupportsKind1[URI, A]):

  @abstractmethod
  def is_empty(self) -> bool:
    ...

  @abstractmethod
  def non_empty(self) -> bool:
    ...


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
