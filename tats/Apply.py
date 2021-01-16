from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1, kinded

from .Op import UnOp

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class Apply(Generic[URI]):

  @staticmethod
  @abstractmethod
  def ap(ff: Kind1[URI, UnOp[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    ...
