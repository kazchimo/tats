from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Literal, cast, Generic, Any

from returns.primitives.hkt import SupportsKind2, Kind1

from tats.Eq import derive_eq
from tats.Monad import Monad, monad_syntax
from tats.Op import UnOp

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")

URI = Literal["Either"]


class EitherInstance(Monad[URI], Generic[L]):

  @staticmethod
  def flat_map(fa: Kind1[URI, A], f: UnOp[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    if fa.is_left():
      return cast(Left[L], fa)
    else:
      return f(fa.value)

  @staticmethod
  def pure(a: R) -> "Either[R, L]":
    return Right(a)


@derive_eq
@monad_syntax(EitherInstance)
class Either(SupportsKind2[URI, R, L]):

  @abstractmethod
  def is_left(self) -> bool:
    ...

  def is_right(self) -> bool:
    return not self.is_left()

  def fold(self, fl: UnOp[L, A], fr: UnOp[R, A]) -> A:
    return fl(cast(Left[L], self).value) \
      if self.is_left() \
      else fr(cast(Right[R], self).value)


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
