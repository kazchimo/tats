from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Literal, cast, Generic, Any, Type

from returns.primitives.hkt import SupportsKind2, Kind1

from tats.Applicative import ApplicativeSyntax, Applicative
from tats.Eq import DeriveEq
from tats.Monad import Monad, monad_syntax
from tats.Op import Func1

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")

URI = Literal["Either"]


class EitherInstance(Monad[URI], Generic[L]):

  @staticmethod
  def flat_map(fa: Kind1[URI, A], f: Func1[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    if fa.is_left():
      return cast(Left[L], fa)
    else:
      return f(fa.value)

  @staticmethod
  def pure(a: R) -> "Either[R, L]":
    return Right(a)


@monad_syntax(EitherInstance)
class Either(SupportsKind2[URI, R, L], DeriveEq, ApplicativeSyntax[URI, R]):

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
  def _self(self) -> "Either[R, L]":
    return self

  @property
  def _applicative_syntax(self) -> Type[Applicative[URI]]:
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
