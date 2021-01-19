from abc import ABC
from typing import TypeVar

from tats.CommutativeSemigroup import CommutativeSemigroup
from tats.Monoid import Monoid

T = TypeVar("T")


class CommutativeMonoid(Monoid[T], CommutativeSemigroup[T], ABC):
  @classmethod
  def reverse(cls) -> "Monoid[T]":
    return cls()
