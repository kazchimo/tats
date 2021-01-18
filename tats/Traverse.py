from abc import abstractmethod
from typing import Generic, TypeVar

from returns.primitives.hkt import Kind1, Kind2, Kind3

from tats.Foldable import Foldable
from tats.Functor import Functor
from tats.data.Function import Func1
from tats.syntax.applicative import HasApplicativeInstance
from tats.syntax.flat_map import HasFlatMapInstance

F = TypeVar("F", bound=Kind1)
G = TypeVar("G", bound=Kind1)
A = TypeVar("A")
B = TypeVar("B")


class Traverse(Generic[F, G], Foldable[F], Functor[F], HasApplicativeInstance[G],
               HasFlatMapInstance[F]):
  @abstractmethod
  def traverse(self, fa: Kind1[F, A], f: Func1[A, Kind1[G, B]]) -> Kind2[G, F, B]:
    ...

  def flat_traverse(self, fa: Kind1[F, A], f: Func1[A, Kind2[G, F, B]]) -> Kind2[G, F, B]:
    def _map(ffa: Kind3[G, F, F, B], \
             ff: Func1[Kind2[F, F, B], Kind1[F, B]]
             ) -> Kind2[G, F, B]:
      return self._applicative_instance.map(ffa, ff)

    def _flatten(ffa: Kind2[F, F, B]) -> Kind1[F, B]:
      return self._flat_map_instance.flatten(ffa)

    return _map(self.traverse(fa, f), _flatten)
