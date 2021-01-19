from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.Applicative import Applicative
from tats.Apply import Apply
from tats.syntax.apply import ApplySyntax, HasApplyInstance

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasApplicativeInstance(Generic[F], HasApplyInstance[F]):
  @staticmethod
  @abstractmethod
  def _applicative_instance() -> Applicative[F]:
    ...

  @classmethod
  def _apply_instance(cls) -> Apply[F]:
    return cls._applicative_instance()


class ApplicativeSyntax(Generic[F, A], ApplySyntax[F, A], HasApplicativeInstance[F]):
  ...
