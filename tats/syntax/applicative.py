from abc import abstractmethod
from typing import Generic, Type, TypeVar

from returns.primitives.hkt import Kind1

from tats.Applicative import Applicative
from tats.Apply import Apply
from tats.syntax.apply import ApplySyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class ApplicativeSyntax(Generic[F, A], ApplySyntax[F, A]):

  @property
  @abstractmethod
  def _applicative_syntax(self) -> Type[Applicative[F]]:
    ...

  @property
  def _apply_instance(self) -> Type[Apply[F]]:
    return self._applicative_syntax
