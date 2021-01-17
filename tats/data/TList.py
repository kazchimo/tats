from typing import Literal, TypeVar, List, Type, Generic

from returns.primitives.hkt import SupportsKind1, Kind1, dekind

from tats.Monad import Monad
from tats.Op import Func1
from tats.Monad import MonadSyntax
from tats.Eq import DeriveEq

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


class TList(SupportsKind1["TList", A], List[A], DeriveEq, MonadSyntax):

  @property
  def _self(self) -> "TList[A]":
    return self

  @property
  def _monad_instance(self) -> Type[Monad["TList"]]:
    return TListInstance
