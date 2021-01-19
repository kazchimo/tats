from dataclasses import dataclass
from typing import cast, Generic, TypeVar

from returns.primitives.hkt import Kind1, Kind2, dekind

from tats.Applicative import Applicative
from tats.FlatMap import FlatMap
from tats.Traverse import Traverse
from tats.data.Function import Func2
from tats.Monad import Monad
from tats.Monoid import Kind1Monoid
from tats.Semigroup import Semigroup
from tats.data.Function import Func1
from tats.data.Option import Option, Some, Nothing

G = TypeVar("G", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class OptionInstance(Monad["Option"], Traverse["Option"]):
  @staticmethod
  def flat_map(fa: Kind1["Option", A], f: Func1[A, Kind1["Option", B]]) -> Kind1["Option", B]:
    return Nothing() if fa.is_empty() else f(cast(Some[A], fa).a)

  @staticmethod
  def pure(a: A) -> "Option[A]":
    return Some(a)

  @staticmethod
  def fold_left(fa: Kind1[Option, A], b: B, f: Func2[B, A, B]) -> B:
    ff: Func1[A, B] = lambda a: f(b, a)
    return dekind(fa).fold(b, ff)

  @property
  def _flat_map_instance(self) -> FlatMap[Option]:
    return self

  def traverse(self, gap: Applicative[G], fa: Kind1[Option, A],\
               f: Func1[A, Kind1[G, B]]) -> Kind2[G, Option, B]:
    if dekind(fa).is_empty():
      return cast(Kind2[G, Option, B], gap.pure(Nothing()))
    else:
      ff: Func1[B, Option[B]] = Some
      return gap.map(f(dekind(fa).get), ff)


@dataclass(frozen=True)
class Kind1OptionInstance(Generic[A], Kind1Monoid["Option", A]):
  @staticmethod
  def combine(tsemi: Semigroup[A], a: "Option[A]", b: "Option[A]") -> "Option[A]":
    if a.non_empty() and b.non_empty():
      return Some(tsemi.combine(a.get, b.get))
    else:
      return Nothing()

  @staticmethod
  def empty() -> "Option[A]":
    return Nothing()
