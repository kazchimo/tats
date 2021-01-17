from abc import abstractmethod
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Apply import Apply, ApplySyntax
from .Op import Func1

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Applicative(Generic[URI], Apply[URI]):

  @classmethod
  def map(cls, fa: Kind1[URI, A], f: Func1[A, B]) -> Kind1[URI, B]:
    return cls.ap(cls.pure(f), fa)

  @staticmethod
  @abstractmethod
  def pure(a: A) -> Kind1[URI, A]:
    ...


class ApplicativeSyntax(Generic[URI, A], ApplySyntax[URI, A]):

  @property
  @abstractmethod
  def _applicative_syntax(self) -> Type[Applicative[URI]]:
    ...

  @property
  def _apply_instance(self) -> Type[Apply[URI]]:
    return self._applicative_syntax
