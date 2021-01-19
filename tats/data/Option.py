from dataclasses import dataclass
from typing import TypeVar, cast, Generic, Any, Type, Optional

from returns.primitives.hkt import SupportsKind1, Kind1

from tats.Traverse import Traverse

from tats.syntax.traverse import TraverseSyntax
from tats.Monad import Monad
from tats.Monoid import Kind1Monoid
from tats.data import Either
from tats.data.Function import Func1
from tats.syntax.eq import DeriveEq
from tats.syntax.monad import MonadSyntax
from tats.syntax.monoid import Kind1MonoidSyntax

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class WithFilter(Generic[A]):
  o: "Option[A]"
  p: Func1[A, bool]

  def map(self, f: Func1[A, B]) -> Kind1["Option", B]:
    return self.o.filter(self.p).map(f)

  def flat_map(self, f: Func1[A, "Option[B]"]) -> Kind1["Option", B]:
    return self.o.filter(self.p).flat_map(f)

  def foreach(self, f: Func1[A, B]) -> None:
    self.o.filter(self.p).foreach(f)

  def with_filter(self, p: Func1[A, bool]) -> "WithFilter[A]":
    return WithFilter(self.o, lambda a: self.p(a) and p(a))


class Option(SupportsKind1["Option", A], DeriveEq, MonadSyntax["Option", A],
             Kind1MonoidSyntax["Option", A], TraverseSyntax["Option"]):
  @staticmethod
  def from_nullable(a: Optional[A]) -> "Option[A]":
    return Nothing() if a is None else Some(a)

  @staticmethod
  def when(cond: bool, a: A) -> "Option[A]":
    return Some(a) if cond else Nothing()

  @staticmethod
  def unless(cond: bool, a: A) -> "Option[A]":
    return Nothing() if cond else Some(a)

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

  def to_right(self, left: B) -> "Either.Either[A, B]":
    from .Either import Left, Right
    return Left(left) if self.is_empty() else Right(self.get)

  def to_left(self, right: B) -> "Either.Either[B, A]":
    from .Either import Left, Right
    return Right(right) if self.is_empty() else Left(self.get)

  @property
  def _self(self) -> "Option[A]":
    return self

  @staticmethod
  def _monad_instance() -> Monad["Option"]:
    from tats.instance.option import OptionInstance
    return OptionInstance()

  @property
  def _monoid_instance(self) -> Kind1Monoid["Option", A]:
    from tats.instance.option import Kind1OptionInstance
    return Kind1OptionInstance()

  @staticmethod
  def _traverse_instance() -> Traverse["Option"]:
    from tats.instance.option import OptionInstance
    return OptionInstance()


@dataclass(frozen=True)
class Some(Option[A]):
  a: A


@dataclass()
class Nothing(Option[Any]):
  ...
