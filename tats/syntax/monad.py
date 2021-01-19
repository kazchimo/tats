from abc import abstractmethod
from typing import Generic, Type, TypeVar

from returns.primitives.hkt import Kind1

from tats.Applicative import Applicative
from tats.FlatMap import FlatMap
from tats.Monad import Monad
from tats.syntax.applicative import ApplicativeSyntax, HasApplicativeInstance
from tats.syntax.flat_map import FlatMapSyntax, HasFlatMapInstance

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasMonadInstance(Generic[F], HasFlatMapInstance[F], HasApplicativeInstance[F]):
  @staticmethod
  @abstractmethod
  def _monad_instance() -> Monad[F]:
    ...

  @classmethod
  def _flat_map_instance(cls) -> FlatMap[F]:
    return cls._monad_instance()

  @classmethod
  def _applicative_instance(cls) -> Applicative[F]:
    return cls._monad_instance()


class MonadSyntax(Generic[F, A], FlatMapSyntax[F, A], ApplicativeSyntax[F, A], HasMonadInstance[F]):
  ...
