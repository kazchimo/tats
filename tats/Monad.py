from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .data.Function import Func1
from .Applicative import Applicative, ApplicativeSyntax
from .FlatMap import FlatMap, FlatMapSyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Monad(Generic[F], FlatMap[F], Applicative[F]):

  @classmethod
  def map(cls, fa: Kind1[F, A], f: Func1[A, B]) -> Kind1[F, B]:
    return cls.flat_map(fa, lambda x: cls.pure(f(x)))


class MonadSyntax(\
  Generic[F, A], FlatMapSyntax[F, A], ApplicativeSyntax[F, A]):

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
