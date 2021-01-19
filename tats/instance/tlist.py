from functools import reduce
from typing import TypeVar, Generic, Type, List, cast

from returns.primitives.hkt import Kind1, dekind, Kind2

from tats.Applicative import Applicative
from tats.FlatMap import FlatMap
from tats.Monad import Monad
from tats.Monoid import Monoid
from tats.Traverse import Traverse
from tats.data.Function import Func1, Func2
from tats.data.TList import TList

G = TypeVar("G", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class TListInstance(Monad["TList"], Traverse["TList"]):
  @staticmethod
  def flat_map(fa: Kind1["TList", A], f: Func1[A, Kind1["TList", B]]) -> Kind1["TList", B]:
    return TList([b for a in dekind(fa) for b in dekind(f(a))])

  @staticmethod
  def pure(a: A) -> Kind1["TList", A]:
    return TList([a])

  def fold_left(self, fa: Kind1["TList", A], b: B, f: Func2[B, A, B]) -> B:
    return reduce(f, fa, b)

  def traverse(self, gap: Applicative[G], fa: Kind1["TList", A],
               f: Func1[A, Kind1[G, B]]) -> Kind2[G, "TList", B]:
    l: List[B] = []
    empty = cast(Kind2[G, "TList", B], gap.pure(TList(l)))
    return self.fold_left(fa, empty, lambda ac, el: gap.map2(ac, f(el), lambda a, b: a + [b]))

  @property
  def _flat_map_instance(self) -> FlatMap["TList"]:
    return self


class TListInstance1(Generic[A], Monoid[TList[A]]):
  @staticmethod
  def combine(a: "TList[A]", b: "TList[A]") -> "TList[A]":
    return a + b

  @property
  def empty(self) -> "TList[A]":
    return TList([])
