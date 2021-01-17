from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1, dekind

from tats.Semigroup import Semigroup
from tats.data.Function import Func1
from tats.Monad import Monad
from tats.data.TList import TList

A = TypeVar("A")
B = TypeVar("B")


class TListInstance(Monad["TList"]):

  @staticmethod
  def flat_map(fa: Kind1["TList", A],
               f: Func1[A, Kind1["TList", B]]) -> Kind1["TList", B]:
    return TList([b for a in dekind(fa) for b in dekind(f(a))])

  @staticmethod
  def pure(a: A) -> Kind1["TList", A]:
    return TList([a])


class TListInstance1(Generic[A], Semigroup[TList[A]]):

  @staticmethod
  def _cmb(a: "TList[A]", b: "TList[A]") -> "TList[A]":
    return a + b
