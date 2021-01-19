from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from tats.data.Function import Func2, Func1, EndoFunc2, Func1F
from tats.data.Option import Option, Nothing, Some

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Foldable(Generic[F]):
  @abstractmethod
  def fold_left(self, fa: Kind1[F, A], b: B, f: Func2[B, A, B]) -> B:
    ...

  def reduce_left_to_option(self, fa: Kind1[F, A], f: Func1[A, B], g: Func2[B, A, B]) -> Option[B]:
    conv: Func2[
      Option[B], A,
      Option[B]] = lambda acc, el: Some(f(el)) if acc.is_empty() else Some(g(acc.get, el))

    return self.fold_left(fa, Nothing(), conv)

  def reduce_left_option(self, fa: Kind1[F, A], f: EndoFunc2[A]) -> Option[A]:
    ff: Func1[A, A] = Func1F.id()
    return self.reduce_left_to_option(fa, ff, f)

  from tats.data import TList

  def to_tlist(self, fa: Kind1[F, A]) -> "TList.TList[A]":
    from tats.data import TList
    return self.fold_left(fa, TList.TList([]), lambda a, b: a + [b])
