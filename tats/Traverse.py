from abc import abstractmethod
from typing import Generic, TypeVar, cast

from returns.primitives.hkt import Kind1, Kind2, Kind3

from tats.Applicative import Applicative
from tats.Foldable import Foldable
from tats.Functor import Functor
from tats.data.Function import Func1, Func2, Func1F
from tats.syntax.flat_map import HasFlatMapInstance

F = TypeVar("F", bound=Kind1)
G = TypeVar("G", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Traverse(Generic[F], Foldable[F], Functor[F], HasFlatMapInstance[F]):
  @staticmethod
  @abstractmethod
  def traverse(gap: Applicative[G], fa: Kind1[F, A], \
               f: Func1[A, Kind1[G, B]]) -> Kind2[G, F, B]:
    ...

  @classmethod
  def flat_traverse(cls, gap: Applicative[G], fa: Kind1[F, A],
                    f: Func1[A, Kind2[G, F, B]]) -> Kind2[G, F, B]:
    _map = cast(
      Func2[Kind3[G, F, F, B], Func1[Kind2[F, F, B], Kind1[F, B]], Kind2[G, F, B]], gap.map)

    _flatten: Func1[Kind2[F, F, B], Kind1[F, B]] = lambda ffa: cls()._flat_map_instance.flatten(ffa)

    return _map(cls.traverse(gap, fa, f), _flatten)

  @classmethod
  def sequence(cls, gap: Applicative[G], fga: Kind2[F, G, A]) -> Kind2[G, F, A]:
    f: Func1[Kind1[G, A], Kind1[G, A]] = Func1F.id()
    return cls.traverse(gap, fga, f)
