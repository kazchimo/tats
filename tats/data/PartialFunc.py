from dataclasses import dataclass
from typing import TypeVar, Generic, List, Union, Tuple, cast, Type, Any

from pampy import match, match_value

from tats.data.Function import Func1

T = TypeVar("T")
S = TypeVar("S")


@dataclass(frozen=True)
class Case(Generic[T, S]):
  when: T
  then: Union[Func1[T, S], S]

  @property
  def to_tuple(self) -> Tuple[T, Union[Func1[T, S], S]]:
    return self.when, self.then


@dataclass(frozen=True)
class PartialFunc(Func1[T, S]):
  cases: List[Case[T, S]]

  @staticmethod
  def cs(*cases: Case[T, S]) -> "PartialFunc[T, S]":
    return PartialFunc(list(cases))

  def run(self, a: T) -> S:
    return cast(S, match(a, *self.__cases()))

  def is_defined_at(self, a: T) -> bool:
    return any([match_value(p, a)[0] for p in self.__whens()])

  def __cases(self) -> List[Union[Func1[T, S], S, T]]:
    return [e for c in self.cases for e in c.to_tuple]

  def __whens(self) -> List[T]:
    return [c.when for c in self.cases]
