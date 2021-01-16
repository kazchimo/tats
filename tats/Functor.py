from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import SupportsKind1

from .Op import UnOp

I = TypeVar("I", bound=str)
A = TypeVar("A")
B = TypeVar("B")
F = TypeVar("F", bound=SupportsKind1)


class Functor(Generic[I]):

  @staticmethod
  @abstractmethod
  def map(fa: SupportsKind1[I, A], f: UnOp[A, B]) -> SupportsKind1[I, B]:
    ...
