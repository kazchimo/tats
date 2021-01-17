from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class SelfIs(Generic[T]):

  @property
  @abstractmethod
  def _self(self) -> T:
    ...
