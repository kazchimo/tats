from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1, Kind2

from tats.Applicative import Applicative
from tats import Foldable, Traverse
from tats.Functor import Functor
from tats.SelfIs import SelfIs
from tats.data.Function import Func1
from tats.syntax.foldable import FoldableSyntax, HasFoldableInstance
from tats.syntax.functor import FunctorSyntax, HasFunctorInstance

F = TypeVar("F", bound=Kind1)
G = TypeVar("G", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasTraverseInstance(Generic[F], HasFoldableInstance[F], HasFunctorInstance[F]):
  @staticmethod
  @abstractmethod
  def _traverse_instance() -> "Traverse.Traverse[F]":
    ...

  @classmethod
  def _foldable_instance(cls) -> "Foldable.Foldable[F]":
    return cls._traverse_instance()

  @classmethod
  def _functor_instance(cls) -> Functor[F]:
    return cls._traverse_instance()


class TraverseSyntax(Generic[F], FoldableSyntax[F], FunctorSyntax[F], HasTraverseInstance[F],
                     SelfIs[F]):
  def traverse(self, gap: Applicative[G], f: Func1[A, Kind1[G, B]]) -> Kind2[G, F, B]:
    return self._traverse_instance().traverse(gap, self._self, f)

  def flat_traverse(self, gap: Applicative[G], f: Func1[A, Kind2[G, F, B]]) -> Kind2[G, F, B]:
    return self._traverse_instance().flat_traverse(gap, self._self, f)

  def sequence(self, gap: Applicative[G]) -> Kind2[G, F, A]:
    return self._traverse_instance().sequence(gap, self._self)
