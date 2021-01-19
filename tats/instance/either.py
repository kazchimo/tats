from typing import Generic, cast, TypeVar

from returns.primitives.hkt import Kind1

from tats.Monad import Monad
from tats.Semigroup import Kind1Semigroup, Semigroup
from tats.data.Either import Either, Left, Right
from tats.data.Function import Func1

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")


class EitherInstance(Monad["Either"], Generic[L]):
  @staticmethod
  def flat_map(fa: Kind1["Either", A], f: Func1[A, Kind1["Either", B]]) -> Kind1["Either", B]:
    if fa.is_left():
      return cast(Left[L], fa)
    else:
      return f(cast(Right[A], fa).value)

  @staticmethod
  def pure(a: R) -> "Either[R, L]":
    return Right(a)


class Kind1EitherInstance(Generic[R], Kind1Semigroup["Either", R]):
  @staticmethod
  def combine(tsemi: Semigroup[R], a: "Either[R, L]", b: "Either[R, L]") -> "Either[R, L]":
    if a.is_left():
      return a
    else:
      if b.is_left():
        return b
      else:
        return Right(tsemi.combine(a.get, b.get))
