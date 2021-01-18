from collections import UserList
from dataclasses import dataclass
from typing import TypeVar, List, Type

from returns.primitives.hkt import SupportsKind1

from tats.Monad import Monad
from tats.Monoid import Monoid
from tats.syntax.eq import DeriveEq
from tats.syntax.monad import MonadSyntax
from tats.syntax.monoid import MonoidSyntax

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class TList(UserList[A], SupportsKind1["TList", A], DeriveEq, MonadSyntax,
            MonoidSyntax["TList[A]"]):
  data: List[A]

  @staticmethod
  def var(*a: A) -> "TList[A]":
    return TList(list(a))

  @property
  def _self(self) -> "TList[A]":
    return self

  @property
  def _monad_instance(self) -> Type[Monad["TList"]]:
    from tats.instance.tlist import TListInstance
    return TListInstance

  @property
  def _monoid_instance(self) -> Monoid["TList[A]"]:
    from tats.instance.tlist import TListInstance1
    return TListInstance1()
