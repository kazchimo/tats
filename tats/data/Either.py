from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, cast, Any

from returns.primitives.hkt import SupportsKind2

from tats import Traverse
from tats.Monad import Monad
from tats.Semigroup import Kind1Semigroup
from tats.data import Option
from tats.data.Function import Func1, Func1F
from tats.syntax.eq import DeriveEq
from tats.syntax.monad import MonadSyntax
from tats.syntax.semigroup import Kind1SemigroupSyntax
from tats.syntax.traverse import TraverseSyntax

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")


class EitherStatic(TraverseSyntax["Either"], MonadSyntax["Either", R]):
  @staticmethod
  def _traverse_instance() -> "Traverse.Traverse[Either]":
    from tats.instance.either import EitherInstance
    return EitherInstance()

  @staticmethod
  def _monad_instance() -> Monad["Either"]:
    from tats.instance.either import EitherInstance
    return EitherInstance()

  @staticmethod
  def cond(test: bool, right: R, left: L) -> "Either[R, L]":
    return Right(right) if test else Left(left)


class Either(SupportsKind2["Either", R, L], DeriveEq, Kind1SemigroupSyntax["Either", R],
             EitherStatic):
  @abstractmethod
  def is_left(self) -> bool:
    ...

  def is_right(self) -> bool:
    return not self.is_left()

  def fold(self, fl: Func1[L, A], fr: Func1[R, A]) -> A:
    return fl(cast(Left[L], self).value) \
      if self.is_left() \
      else fr(cast(Right[R], self).value)

  @property
  def swap(self) -> "Either[L, R]":
    return self.fold(Right, Left)

  def foreach(self, f: Func1[R, A]) -> None:
    self.fold(Func1F.id(), f)

  @property
  def get(self) -> R:
    if self.is_left():
      raise ValueError("cannot get from Left")
    else:
      return cast(Right[R], self).value

  def get_or_else(self, _or: R) -> R:
    return self.fold(Func1F.const(_or), Func1F.id())

  def or_else(self, fallback: "Either[R, A]") -> "Either[R, A]":
    return self.fold(Func1F.const(fallback), lambda a: Right(a))

  def contains(self, e: R) -> bool:
    return self.fold(Func1F.false(), Func1F.eq(e))

  def forall(self, p: Func1[R, bool]) -> bool:
    return self.fold(Func1F.true(), p)

  def exists(self, p: Func1[R, bool]) -> bool:
    return self.fold(Func1F.false(), p)

  def value_or(self, f: Func1[L, R]) -> R:
    return self.fold(f, Func1F.id())

  def ensure(self, on_failure: L, f: Func1[R, bool]) -> "Either[R, L]":
    if self.is_left():
      return self
    else:
      return self if f(self.get) else Left(on_failure)

  def to_option(self) -> "Option.Option[R]":
    from tats.data.Option import Nothing, Some
    return self.fold(Func1F.const(Nothing()), Some)

  def _semigroup_instance(self) -> Kind1Semigroup["Either", R]:
    from tats.instance.either import Kind1EitherInstance
    return Kind1EitherInstance()


@dataclass(frozen=True)
class Left(Either[Any, L]):
  value: L

  def is_left(self) -> bool:
    return True


@dataclass(frozen=True)
class Right(Either[R, Any]):
  value: R

  def is_left(self) -> bool:
    return False
