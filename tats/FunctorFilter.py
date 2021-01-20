from abc import abstractmethod
from typing import TypeVar, Generic

from returns.primitives.hkt import Kind1, Kind2

from tats.data import PartialFunc
from tats.data import Option
from tats.data.Function import Func1

F = TypeVar("F", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class FunctorFilter(Generic[F]):
  @staticmethod
  @abstractmethod
  def map_filter(fa: Kind1[F, A], f: Func1[A, "Option.Option[B]"]) -> Kind1[F, B]:
    ...

  @classmethod
  def collect(cls, fa: Kind1[F, A], f: "PartialFunc.PartialFunc[A, B]") -> Kind1[F, B]:
    return cls.map_filter(fa, f.lift)

  @classmethod
  def flatten_option(cls, fa: Kind2[F, "Option.Option", A]) -> Kind1[F, A]:
    return cls.map_filter(fa, lambda x: x)

  @classmethod
  def filter(cls, fa: Kind1[F, A], f: Func1[A, bool]) -> Kind1[F, A]:
    from tats.data.Option import Some, Nothing
    return cls.map_filter(fa, lambda a: Some(a) if f(a) else Nothing())

  @classmethod
  def filter_not(cls, fa: Kind1[F, A], f: Func1[A, bool]) -> Kind1[F, A]:
    from tats.data.Option import Some, Nothing
    return cls.map_filter(fa, lambda a: Nothing() if f(a) else Some(a))
