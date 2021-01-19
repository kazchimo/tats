from collections import UserList
from dataclasses import dataclass
from typing import TypeVar, List, Type, Tuple

from returns.primitives.hkt import SupportsKind1

from tats import Foldable
from tats.Monad import Monad
from tats.Monoid import Monoid
from tats.Traverse import Traverse
from tats.data.Function import Func1
from tats.syntax.eq import DeriveEq
from tats.syntax.monad import MonadSyntax
from tats.syntax.monoid import MonoidSyntax
from tats.syntax.traverse import TraverseSyntax, F

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class TList(UserList[A], SupportsKind1["TList", A], DeriveEq, MonadSyntax, MonoidSyntax["TList[A]"],
            TraverseSyntax["TList"]):
  data: List[A]

  @property
  def head(self) -> A:
    if len(self.data) == 0:
      raise ValueError("head of empty TList")
    else:
      return self.data[0]

  @property
  def tail(self) -> "TList[A]":
    if len(self.data) == 0:
      raise ValueError("head of empty TList")
    else:
      return TList(self.data[1:])

  def take(self, n: int) -> "TList[A]":
    return TList(self.data[:n]) if n > 0 else TList([])

  def drop(self, n: int) -> "TList[A]":
    return TList(self.data[n:]) if n > 0 else self

  def take_right(self, n: int) -> "TList[A]":
    return TList(self.data[-n:]) if n > 0 else TList([])

  def split_at(self, n: int) -> Tuple["TList[A]", "TList[A]"]:
    return (TList(self.data[:n]), TList(self.data[n:])) \
      if n > 0\
      else (TList([]), self)

  def take_while(self, p: Func1[A, bool]) -> "TList[A]":
    l: List[A] = []
    these = self

    while these.non_empty and p(these.head):
      l = l + [these.head]
      these = these.tail

    return TList(l)

  def drop_while(self, p: Func1[A, bool]) -> "TList[A]":
    these = self
    while these.non_empty and p(these.head):
      these = these.tail

    return these

  def span(self, p: Func1[A, bool]) -> Tuple["TList[A]", "TList[A]"]:
    l: List[A] = []
    these = self

    while these.non_empty and p(these.head):
      l = l + [these.head]
      these = these.tail

    return TList(l), these

  @staticmethod
  def var(*a: A) -> "TList[A]":
    return TList(list(a))

  @property
  def _monad_instance(self) -> Monad["TList"]:
    from tats.instance.tlist import TListInstance
    return TListInstance()

  @property
  def _monoid_instance(self) -> Monoid["TList[A]"]:
    from tats.instance.tlist import TListInstance1
    return TListInstance1()

  @property
  def _traverse_instance(self) -> Traverse["TList[A]"]:
    from tats.instance.tlist import TListInstance
    return TListInstance()
