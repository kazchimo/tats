from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Op import Func1
from .Applicative import Applicative, ApplicativeSyntax
from .FlatMap import FlatMap, FlatMapSyntax

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Monad(Generic[URI], FlatMap[URI], Applicative[URI]):

  @classmethod
  def map(cls, fa: Kind1[URI, A], f: Func1[A, B]) -> Kind1[URI, B]:
    return cls.flat_map(fa, lambda x: cls.pure(f(x)))


class MonadSyntax(\
  Generic[URI, A], FlatMapSyntax[URI, A], ApplicativeSyntax[URI, A]):

  @property
  @abstractmethod
  def _monad_instance(self) -> Type[Monad[URI]]:
    ...

  @property
  def _flat_map_instance(self) -> Type[FlatMap[URI]]:
    return self._monad_instance

  @property
  def _applicative_syntax(self) -> Type[Applicative[URI]]:
    return self._monad_instance
