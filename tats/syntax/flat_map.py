from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Type

from returns.primitives.hkt import Kind1

from tats.Apply import Apply
from tats.FlatMap import FlatMap
from tats.data.Function import Func1
from tats.syntax.apply import ApplySyntax

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasFlatMapInstance(Generic[F]):
  @property
  @abstractmethod
  def _flat_map_instance(self) -> FlatMap[F]:
    ...


class FlatMapSyntax(Generic[F, A], ApplySyntax[F, A], HasFlatMapInstance[F]):
  def flat_map(self, f: Func1[A, Kind1[F, B]]) -> Kind1[F, B]:
    return self._flat_map_instance.flat_map(self._self, f)

  @property
  def _apply_instance(self) -> Apply[F]:
    return self._flat_map_instance
