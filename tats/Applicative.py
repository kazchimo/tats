from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from tats.syntax.apply import ApplySyntax
from .Apply import Apply
from .data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Applicative(Generic[F], Apply[F]):

  @classmethod
  def map(cls, fa: Kind1[F, A], f: Func1[A, B]) -> Kind1[F, B]:
    return cls.ap(cls.pure(f), fa)

  @staticmethod
  @abstractmethod
  def pure(a: A) -> Kind1[F, A]:
    ...


class ApplicativeSyntax(Generic[F, A], ApplySyntax[F, A]):

  @property
  @abstractmethod
  def _applicative_syntax(self) -> Type[Applicative[F]]:
    ...

  @property
  def _apply_instance(self) -> Type[Apply[F]]:
    return self._applicative_syntax
