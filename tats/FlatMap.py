from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from .Op import Func1
from .Apply import Apply, ApplySyntax

URI = TypeVar("URI", bound=str)
A = TypeVar("A")
B = TypeVar("B")


class FlatMap(Generic[URI], Apply[URI]):

  @staticmethod
  @abstractmethod
  def flat_map(fa: Kind1[URI, A], f: Func1[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    ...

  @classmethod
  def flatten(cls, ffa: Kind1[URI, Kind1[URI, A]]) -> Kind1[URI, A]:
    return cls.flat_map(ffa, lambda x: x)

  @classmethod
  def ap(cls, ff: Kind1[URI, Func1[A, B]], fa: Kind1[URI, A]) -> Kind1[URI, B]:
    return cls.flat_map(ff, lambda f: cls.map(fa, f))


class FlatMapSyntax(Generic[URI, A], ApplySyntax[URI, A], ABC):

  def flat_map(self, f: Func1[A, Kind1[URI, B]]) -> Kind1[URI, B]:
    return self._flat_map_instance.flat_map(self._self, f)

  @property
  @abstractmethod
  def _flat_map_instance(self) -> Type[FlatMap[URI]]:
    ...

  @property
  def _apply_instance(self) -> Type[Apply[URI]]:
    return self._flat_map_instance
