from typing import Generic, TypeVar

T = TypeVar("T")


class Show(Generic[T]):
  @staticmethod
  def show(a: T) -> str:
    ...
