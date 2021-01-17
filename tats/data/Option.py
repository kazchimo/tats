from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Literal, NoReturn, cast

from returns.primitives.hkt import SupportsKind1, Kind1

from tats.Eq import derive_eq
from tats.Monad import monad_syntax, Monad
from tats.Op import UnOp

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

  @property
  def get(self) -> A:
    if self.non_empty():
      return cast(Some[A], self).a
    else:
      raise ValueError("No elements inside Nothing")

  def get_or_else(self, default: A) -> A:
    return self.get if self.non_empty() else default

  def fold(self, if_empty: B, f: UnOp[A, B]) -> B:
    return f(self.get) if self.non_empty() else if_empty

  def filter(self, p: UnOp[A, bool]) -> "Option[A]":
    return self if self.is_empty() or p(self.get) else Nothing()

  def filter_not(self, p: UnOp[A, bool]) -> "Option[A]":
    return self if self.is_empty() or not p(self.get) else Nothing()


  def foreach(self, f: UnOp[A, B]) -> None:
    if self.non_empty():
      f(self.get)

@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False


@dataclass()
class Nothing(Option[NoReturn]):

  def is_empty(self) -> bool:
    return True
