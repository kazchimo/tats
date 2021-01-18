from functools import reduce
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1, dekind

from tats.Foldable import Foldable, F
from tats.Monad import Monad
from tats.Monoid import Monoid
from tats.data.Function import Func1, Func2
from tats.data.TList import TList

A = TypeVar("A")
B = TypeVar("B")


class TListInstance(Monad["TList"], Foldable["TList"]):
  @staticmethod
  def flat_map(fa: Kind1["TList", A], f: Func1[A, Kind1["TList", B]]) -> Kind1["TList", B]:
    return TList([b for a in dekind(fa) for b in dekind(f(a))])

  @staticmethod
  def pure(a: A) -> Kind1["TList", A]:
    return TList([a])

  def fold_left(self, fa: Kind1[F, A], b: B, f: Func2[B, A, B]) -> B:
    return reduce(f, fa, b)


class TListInstance1(Generic[A], Monoid[TList[A]]):
  @staticmethod
  def combine(a: "TList[A]", b: "TList[A]") -> "TList[A]":
    return a + b

  @property
  def empty(self) -> "TList[A]":
    return TList([])
