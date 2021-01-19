from dataclasses import dataclass
from dataclasses import dataclass
from typing import TypeVar, List, Tuple, Iterator, Sequence, overload

from returns.primitives.hkt import SupportsKind1

from tats import Traverse
from tats.Monad import Monad
from tats.Monoid import Monoid
from tats.data.Function import Func1
from tats.syntax.eq import DeriveEq
from tats.syntax.monad import MonadSyntax
from tats.syntax.monoid import MonoidSyntax
from tats.syntax.traverse import TraverseSyntax

A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True)
class TList(Sequence[A], SupportsKind1["TList", A], DeriveEq, MonadSyntax, MonoidSyntax["TList"],
            TraverseSyntax["TList"]):
  data: List[A]

  @property
  def size(self) -> int:
    return len(self.data)

  @property
  def reverse(self) -> "TList[A]":
    return TList(self.data[::-1])

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

  def __iter__(self) -> Iterator[A]:
    i = 0
    while i <= self.size - 1:
      v = self.data[i]
      yield v
      i = i + 1

    return

  @overload
  def __getitem__(self, i: int) -> A:
    ...

  @overload
  def __getitem__(self, s: slice) -> "TList[A]":
    ...

  def __getitem__(self, a):
    if isinstance(a, int):
      return self.data[a]
    else:
      return TList(self.data[a])

  def __len__(self) -> int:
    return len(self.data)

  @property
  def _monad_instance(self) -> Monad["TList"]:
    from tats.instance.tlist import TListInstance
    return TListInstance()

  @property
  def _monoid_instance(self) -> Monoid["TList[A]"]:
    from tats.instance.tlist import TListInstance1
    return TListInstance1()

  @property
  def _traverse_instance(self) -> "Traverse.Traverse[TList[A]]":
    from tats.instance.tlist import TListInstance
    return TListInstance()
