from abc import ABC
from typing import TypeVar

from tats.Semigroup import Semigroup

T = TypeVar("T")


class CommutativeSemigroup(Semigroup[T], ABC):
  @classmethod
  def reverse(cls) -> "Semigroup[T]":
    return cls()
