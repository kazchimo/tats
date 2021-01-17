from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Literal, cast, Generic, Any, Type

from returns.primitives.hkt import SupportsKind1, Kind1

from tats.Apply import ApplySyntax, Apply
from tats.Eq import DeriveEq
from tats.Monad import monad_syntax, Monad
from tats.Op import Func1
from .Either import Either, Left, Right

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class OptionInstance(Monad[URI]):

  @staticmethod
  def flat_map(fa: Kind1[URI, A], f: Func1[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    return Nothing() if fa.is_empty() else f(fa.a)

  @staticmethod
  def pure(a: A) -> "Option[A]":
    return Some(a)


@dataclass(frozen=True)
class WithFilter(Generic[A]):
  o: "Option[A]"
  p: Func1[A, bool]

  def map(self, f: Func1[A, B]) -> Kind1[URI, B]:
    return self.o.filter(self.p).map(f)

  def flat_map(self, f: Func1[A, "Option[B]"]) -> "Option[B]":
    return self.o.filter(self.p).flat_map(f)

  def foreach(self, f: Func1[A, B]) -> None:
    self.o.filter(self.p).foreach(f)

  def with_filter(self, p: Func1[A, bool]) -> "WithFilter[A]":
    return WithFilter(self.o, lambda a: self.p(a) and p(a))


@monad_syntax(OptionInstance)
class Option(SupportsKind1[URI, A], DeriveEq, ApplySyntax[URI, A]):

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

  def fold(self, if_empty: B, f: Func1[A, B]) -> B:
    return f(self.get) if self.non_empty() else if_empty

  def filter(self, p: Func1[A, bool]) -> "Option[A]":
    return self if (self.is_empty() or p(self.get)) else Nothing()

  def filter_not(self, p: Func1[A, bool]) -> "Option[A]":
    return self if self.is_empty() or not p(self.get) else Nothing()

  def with_filter(self, p: Func1[A, bool]) -> "WithFilter":
    return WithFilter(self, p)

  def foreach(self, f: Func1[A, B]) -> None:
    if self.non_empty():
      f(self.get)

  def contains(self, e: A) -> bool:
    return self.non_empty() and self.get == e

  def exists(self, p: Func1[A, bool]) -> bool:
    return self.non_empty() and p(self.get)

  def forall(self, p: Func1[A, bool]) -> bool:
    return self.is_empty() or p(self.get)

  def to_right(self, left: B) -> Either[A, B]:
    return Left(left) if self.is_empty() else Right(self.get)

  def to_left(self, right: B) -> Either[B, A]:
    return Right(right) if self.is_empty() else Left(self.get)

  @property
  def _self(self) -> "Option[A]":
    return self

  @property
  def _apply_instance(self) -> Type[Apply[URI]]:
    return OptionInstance


@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False


@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True
