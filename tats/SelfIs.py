from typing import Generic, TypeVar, cast

T = TypeVar("T")


class SelfIs(Generic[T]):

  @property
  def _self(self) -> T:
    return cast(T, self)
