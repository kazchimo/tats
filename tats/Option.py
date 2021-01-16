from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Literal

from returns.primitives.hkt import SupportsKind1, Kind1

from .Applicative import Applicative
from .Eq import derive_eq
from .Monad import monad_syntax, Monad
from .Op import UnOp

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class OptionInstance(Monad[URI]):

  @staticmethod
  def flat_map(fa: Kind1[URI, A], f: UnOp[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    return Nothing() if fa.is_empty() else f(fa.a)

  @staticmethod
  def pure(a: A) -> Kind1[URI, A]:
    return Some(a)


@derive_eq
@monad_syntax(OptionInstance)
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
