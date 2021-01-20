from dataclasses import dataclass
from typing import TypeVar, Generic, List, Union, Tuple, cast, Type, Any

from pampy import match, match_value

from tats.data import Option
from tats.data.Function import Func1

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")


@dataclass(frozen=True)
class Case(Generic[T, S]):
  when: T
  then: Union[Func1[T, S], S]

  @property
  def to_tuple(self) -> Tuple[T, Union[Func1[T, S], S]]:
    return self.when, self.then

  def map(self, f: Func1[S, U]) -> "Case[T, U]":
    """map the Case's `then` result with f"""
    if isinstance(self.then, Func1):
      return Case(self.when, lambda a: f(self.then(a)))
    else:
      return Case(self.when, f(self.then))


@dataclass(frozen=True)
class PartialFunc(Func1[T, S]):
  """
  Partial function wrapping pampy
  """
  cases: List[Case[T, S]]

  @staticmethod
  def cs(*cases: Case[T, S]) -> "PartialFunc[T, S]":
    return PartialFunc(list(cases))

  def run(self, a: T) -> S:
    return cast(S, match(a, *self.__cases()))

  def or_else(self, p: "PartialFunc[T, S]") -> "PartialFunc[T, S]":
    return PartialFunc(self.cases + p.cases)

  def and_then(self, f: Func1[S, U]) -> "PartialFunc[T, U]":
    return PartialFunc([c.map(f) for c in self.cases])

  @property
  def lift(self) -> "Func1[T, Option.Option[S]]":
    """lift this PartialFunc to a plain function returning an Option result"""
    from tats.data.Option import Nothing, Some
    return lambda a: Some(self.run(a)) if self.is_defined_at(a) else Nothing()

  def is_defined_at(self, a: T) -> bool:
    return any([match_value(p, a)[0] for p in self.__whens()])

  def __cases(self) -> List[Union[Func1[T, S], S, T]]:
    return [e for c in self.cases for e in c.to_tuple]

  def __whens(self) -> List[T]:
    return [c.when for c in self.cases]
