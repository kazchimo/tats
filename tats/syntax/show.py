from typing import TypeVar, Generic

from tats.SelfIs import SelfIs
from tats.Show import Show

T = TypeVar("T")


class HasShowInstance(Generic[T]):
  @staticmethod
  def _show_instance() -> Show[T]:
    ...


class ShowSyntax(Generic[T], HasShowInstance[T], SelfIs[T]):
  def show(self) -> str:
    return self._show_instance().show(self._self)


class DeriveShow(ShowSyntax[T]):
  @staticmethod
  def _show_instance() -> Show[T]:
    return Show.instance(str)
