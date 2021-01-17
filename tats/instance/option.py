from dataclasses import dataclass
from typing import cast, Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.Semigroup import Kind1Semigroup, Semigroup
from tats.Monad import Monad
from tats.data.Function import Func1
from tats.data.Option import Option, Some, Nothing

A = TypeVar("A")
B = TypeVar("B")


class OptionInstance(Monad["Option"]):

  @staticmethod
  def flat_map(fa: Kind1["Option", A],
               f: Func1[A, Kind1["Option", B]]) -> Kind1["Option", B]:
    return Nothing() if fa.is_empty() else f(cast(Some[A], fa).a)

  @staticmethod
  def pure(a: A) -> "Option[A]":
    return Some(a)


@dataclass(frozen=True)
class Kind1OptionInstance(Generic[A], Kind1Semigroup["Option", A]):

  @staticmethod
  def _cmb(tsemi: Semigroup[A], a: "Option[A]", b: "Option[A]"):
    if a.non_empty() and b.non_empty():
      return Some(tsemi.combine(a.get, b.get))
    else:
      return Nothing()
