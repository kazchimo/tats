from abc import ABC
from typing import TypeVar

from tats.Semigroup import Semigroup

T = TypeVar("T")


class CommutativeSemigroup(Semigroup[T], ABC):
  def reverse(self) -> "Semigroup[T]":
    return self
