from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1

from tats.SelfIs import SelfIs
from tats.data.Function import Func1
from tats.FunctorFilter import FunctorFilter
from tats.data import PartialFunc, Option

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class HasFunctorFilterInstance(Generic[F]):
  @staticmethod
  @abstractmethod
  def _functor_filter_instance() -> FunctorFilter[F]:
    ...


class FunctorFilterSyntax(Generic[F], SelfIs[F], HasFunctorFilterInstance[F]):
  def map_filter(self, f: Func1[A, "Option.Option[B]"]) -> Kind1[F, B]:
    return self._functor_filter_instance().map_filter(self._self, f)

  def collect(self, f: "PartialFunc.PartialFunc[A, B]") -> Kind1[F, B]:
    return self._functor_filter_instance().collect(self._self, f)

  def filter(self, f: Func1[A, bool]) -> Kind1[F, A]:
    return self._functor_filter_instance().filter(self._self, f)

  def filter_not(self, f: Func1[A, bool]) -> Kind1[F, A]:
    return self._functor_filter_instance().filter_not(self._self, f)
