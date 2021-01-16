from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from .Op import UnOp
from .Apply import Apply

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class FlatMap(Generic[URI], Apply[URI]):

  @staticmethod
  @abstractmethod
  def flat_map(fa: Kind1[URI, A], f: UnOp[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    ...

  @classmethod
  def flatten(cls, ffa: Kind1[URI, Kind1[URI, A]]) -> Kind1[URI, A]:
    return cls.flat_map(ffa, lambda x: x)
