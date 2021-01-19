from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.Apply import Apply
from tats.FlatMap import FlatMap
from tats.data.Function import Func1
from tats.syntax.apply import ApplySyntax, HasApplyInstance

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasFlatMapInstance(Generic[F], HasApplyInstance[F]):
  @staticmethod
  @abstractmethod
  def _flat_map_instance() -> FlatMap[F]:
    ...

  @classmethod
  def _apply_instance(cls) -> Apply[F]:
    return cls._flat_map_instance()


class FlatMapSyntax(Generic[F, A], ApplySyntax[F, A], HasFlatMapInstance[F]):
  def flat_map(self, f: Func1[A, Kind1[F, B]]) -> Kind1[F, B]:
    return self._flat_map_instance().flat_map(self._self, f)
