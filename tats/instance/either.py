from typing import Generic, cast, TypeVar

from returns.primitives.hkt import Kind1, Kind2, dekind

from tats.Applicative import Applicative
from tats.FlatMap import FlatMap
from tats.data.Function import Func2, Func1F
from tats.Traverse import Traverse
from tats.Monad import Monad
from tats.Semigroup import Kind1Semigroup, Semigroup
from tats.data.Either import Either, Left, Right
from tats.data.Function import Func1

L = TypeVar("L")
R = TypeVar("R")
A = TypeVar("A")
B = TypeVar("B")
G = TypeVar("G", bound=Kind1)


class EitherInstance(Monad["Either"], Traverse["Either"], Generic[L]):
  @staticmethod
  def flat_map(fa: Kind1["Either", A], f: Func1[A, Kind1["Either", B]]) -> Kind1["Either", B]:
    if fa.is_left():
      return cast(Left[L], fa)
    else:
      return f(cast(Right[A], fa).value)

  @staticmethod
  def pure(a: R) -> "Either[R, L]":
    return Right(a)

  @staticmethod
  def traverse(gap: Applicative[G], fa: Kind1["Either", A],
               f: Func1[A, Kind1[G, B]]) -> Kind2[G, "Either", B]:
    if dekind(fa).is_left():
      return cast(Kind2[G, Either, B], gap.pure(fa))
    else:
      return gap.map(f(dekind(fa).get), Right)

  @staticmethod
  def fold_left(fa: Kind1["Either", A], b: B, f: Func2[B, A, B]) -> B:
    return dekind(fa).fold(Func1F.const(b), lambda r: f(b, r))

  @classmethod
  def _flat_map_instance(cls) -> FlatMap["Either"]:
    return cls()


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
