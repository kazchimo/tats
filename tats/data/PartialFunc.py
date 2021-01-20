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

  Examples:
    An example corresponding to pampy's one

    >>> from pampy import _
    >>> PartialFunc.cs(
    ...   Case(3, "this matches the number 3"),
    ...   Case(int, "matches any integer"),
    ...   Case((str, int), lambda a, b: "a tuple (a, b) you can use in a function"),
    ...   Case([1, 2, _], "any list of 3 elements that begins with [1, 2]"),
    ...   Case({"x": _}, "any dict with a key 'x' and any value associated"),
    ...   Case(_, "anything else")
    ... ).run(4)
    "matches any integer"
  """
  cases: List[Case[T, S]]

  @staticmethod
  def cs(*cases: Case[T, S]) -> "PartialFunc[T, S]":
    """Constructs PartialFunc from Case varargs"""
    return PartialFunc(list(cases))

  def run(self, a: T) -> S:
    """apply this function to `a`"""
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

  def run_or_else(self, a: T, default: Func1[T, S]) -> S:
    """run this PartialFunc with `default` fallback function"""
    return self.run(a) if self.is_defined_at(a) else default(a)

  def is_defined_at(self, a: T) -> bool:
    return any([match_value(p, a)[0] for p in self.__whens()])

  def __cases(self) -> List[Union[Func1[T, S], S, T]]:
    return [e for c in self.cases for e in c.to_tuple]

  def __whens(self) -> List[T]:
    return [c.when for c in self.cases]
