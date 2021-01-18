from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from tats.Foldable import Foldable
from tats.SelfIs import SelfIs
from tats.data.Function import Func1, Func2, EndoFunc2
from tats.data.Option import Option

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasFoldableInstance(Generic[F]):
  @property
  @abstractmethod
  def _foldable_instance(self) -> Foldable[F]:
    ...


class FoldableSyntax(Generic[F, A], HasFoldableInstance[F], SelfIs[F]):
  def fold_left(self, b: B, f: Func2[B, A, B]) -> B:
    return self._foldable_instance.fold_left(self._self, b, f)

  def reduce_left_to_option(self, f: Func1[A, B], g: Func2[B, A, B]) -> Option[B]:
    return self._foldable_instance.reduce_left_to_option(self._self, f, g)

  def reduce_left_option(self, f: EndoFunc2[A]) -> Option[A]:
    return self._foldable_instance.reduce_left_option(self._self, f)

  from tats.data import TList

  def to_tlist(self) -> "TList.TList[A]":
    return self._foldable_instance.to_tlist(self._self)
