from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Literal, cast, Generic, Any, Type

from returns.primitives.hkt import SupportsKind2, Kind1

from tats.data import Option
from tats.Eq import DeriveEq
from tats.Monad import Monad, MonadSyntax
from tats.Op import Func1

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")


class EitherInstance(Monad["Either"], Generic[L]):

  @staticmethod
  def flat_map(fa: Kind1["Either", A],
               f: Func1[A, Kind1["Either", B]]) -> Kind1["Either", B]:
    if fa.is_left():
      return cast(Left[L], fa)
    else:
      return f(cast(Right[A], fa).value)

  @staticmethod
  def pure(a: R) -> "Either[R, L]":
    return Right(a)


class Either(SupportsKind2["Either", R, L], DeriveEq, MonadSyntax["Either", R]):

  @staticmethod
  def cond(test: bool, right: R, left: L) -> "Either[R, L]":
    return Right(right) if test else Left(left)

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
    self.fold(lambda x: x, lambda x: f(x))

  def get_or_else(self, _or: R) -> R:
    get: Func1[R, R] = lambda x: x
    return self.fold(lambda _: _or, get)

  def contains(self, e: R) -> bool:
    eq: Func1[R, bool] = lambda x: x == e
    return self.fold(lambda _: False, eq)

  def forall(self, p: Func1[R, bool]) -> bool:
    return self.fold(lambda _: True, p)

  def exists(self, p: Func1[R, bool]) -> bool:
    return self.fold(lambda _: False, p)

  def to_option(self) -> "Option.Option[R]":
    from tats.data.Option import Nothing, Some
    return self.fold(lambda _: Nothing(), Some)

  @property
  def _self(self) -> "Either[R, L]":
    return self

  @property
  def _monad_instance(self) -> Type[Monad["Either"]]:
    return EitherInstance


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
