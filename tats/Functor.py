from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1

from .Op import UnOp

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Functor(Generic[URI]):

  @staticmethod
  @abstractmethod
  def map(fa: Kind1[URI, A], f: UnOp[A, B]) -> Kind1[URI, B]:
    ...
