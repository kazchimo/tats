from abc import abstractmethod
from typing import Generic, Type, TypeVar

from returns.primitives.hkt import Kind1

from tats.Applicative import Applicative
from tats.FlatMap import FlatMap
from tats.Monad import Monad
from tats.syntax.applicative import ApplicativeSyntax
from tats.syntax.flat_map import FlatMapSyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class MonadSyntax(Generic[F, A], FlatMapSyntax[F, A], ApplicativeSyntax[F, A]):
  @property
  @abstractmethod
  def _monad_instance(self) -> Type[Monad[F]]:
    ...

  @property
  def _flat_map_instance(self) -> Type[FlatMap[F]]:
    return self._monad_instance

  @property
  def _applicative_syntax(self) -> Type[Applicative[F]]:
    return self._monad_instance
