from abc import ABC
from typing import TypeVar

from tats.CommutativeSemigroup import CommutativeSemigroup
from tats.Monoid import Monoid

T = TypeVar("T")


class CommutativeMonoid(Monoid[T], CommutativeSemigroup[T], ABC):
  def reverse(self) -> "Monoid[T]":
    return self
