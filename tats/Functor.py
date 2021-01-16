from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import SupportsKind1

from .Op import UnOp

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")
F = TypeVar("F", bound=SupportsKind1)


class Functor(Generic[URI]):

  @staticmethod
  @abstractmethod
  def map(fa: SupportsKind1[URI, A], f: UnOp[A, B]) -> SupportsKind1[URI, B]:
    ...
