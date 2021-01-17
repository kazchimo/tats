from collections import UserList
from dataclasses import dataclass
from typing import TypeVar, List, Type, Generic

from returns.primitives.hkt import SupportsKind1, Kind1, dekind

from tats.Eq import DeriveEq
from tats.Monad import Monad
from tats.Monad import MonadSyntax
from tats.Semigroup import Semigroup, SemigroupSyntax
from .Function import Func1

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


@dataclass(frozen=True)
class TList(UserList[A], SupportsKind1["TList", A], DeriveEq, MonadSyntax,
            SemigroupSyntax["TList[A]"]):
  data: List[A]

  @staticmethod
  def var(*a: A) -> "TList[A]":
    return TList(list(a))

  @property
  def _self(self) -> "TList[A]":
    return self

  @property
  def _monad_instance(self) -> Type[Monad["TList"]]:
    return TListInstance

  @property
  def _semigroup_instance(self) -> Semigroup["TList[A]"]:
    return TListInstance1()


class TListInstance1(Generic[A], Semigroup[TList[A]]):

  @staticmethod
  def _cmb(a: "TList[A]", b: "TList[A]") -> "TList[A]":
    return a + b
