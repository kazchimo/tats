from typing import Generic, TypeVar

from tats.data.Function import Func1

T = TypeVar("T")


class Show(Generic[T]):
  @staticmethod
  def show(a: T) -> str:
    ...

  @staticmethod
  def instance(f: Func1[T, str]) -> "Show[T]":
    class _Show(Show[T]):
      @staticmethod
      def show(a: T) -> str:
        return f(a)

    return _Show()
