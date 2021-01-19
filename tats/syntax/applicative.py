from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.Applicative import Applicative
from tats.Apply import Apply
from tats.syntax.apply import ApplySyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasApplicativeInstance(Generic[F]):
  @property
  @abstractmethod
  def _applicative_instance(self) -> Applicative[F]:
    ...


class ApplicativeSyntax(Generic[F, A], ApplySyntax[F, A], HasApplicativeInstance[F]):
  @property
  def _apply_instance(self) -> Apply[F]:
    return self._applicative_instance
