from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from tats.data.Function import Func2, Func1, EndoFunc2, Func1F
from tats.data import Option

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Foldable(Generic[F]):
  @staticmethod
  @abstractmethod
  def fold_left(fa: Kind1[F, A], b: B, f: Func2[B, A, B]) -> B:
    ...

  @classmethod
  def reduce_left_to_option(
      cls, fa: Kind1[F, A], f: Func1[A, B], g: Func2[B, A, B]) -> "Option.Option[B]":
    from tats.data.Option import Option, Nothing, Some
    conv: Func2[
      Option[B], A,
      Option[B]] = lambda acc, el: Some(f(el)) if acc.is_empty() else Some(g(acc.get, el))

    return cls.fold_left(fa, Nothing(), conv)

  @classmethod
  def reduce_left_option(cls, fa: Kind1[F, A], f: EndoFunc2[A]) -> "Option.Option[A]":
    ff: Func1[A, A] = Func1F.id()
    return cls.reduce_left_to_option(fa, ff, f)

  from tats.data import TList

  @classmethod
  def to_tlist(cls, fa: Kind1[F, A]) -> "TList.TList[A]":
    from tats.data import TList
    return cls.fold_left(fa, TList.TList([]), lambda a, b: a.combine(TList.TList([b])))
