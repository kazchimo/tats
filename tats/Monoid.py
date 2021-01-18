from abc import ABC, abstractmethod
from typing import TypeVar

from returns.primitives.hkt import Kind1

from .Semigroup import Semigroup, Kind1Semigroup

T = TypeVar("T")
S = TypeVar("S", bound=Kind1)


class Monoid(Semigroup[T], ABC):

  @property
  @abstractmethod
  def empty(self) -> T:
    ...


class Kind1Monoid(Kind1Semigroup[S, T]):

  @abstractmethod
  def empty(self) -> S:
    ...
