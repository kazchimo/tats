from dataclasses import dataclass
from typing import TypeVar, Generic, List, Union, Tuple, cast, Any

from pampy import match, match_value

from tats.data import Option
from tats.data.Function import Func1

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True, eq=False)
class Case(Generic[T, S]):
  """
  Represents case section in a partial function.
  If `when` is tuple Tuple1 ~ Tuple3 is supported.
  """
  when: Any
  then: Func1[T, S]

  @property
  def to_runnable(self) -> Tuple[Any, Any]:
    """Converts `Case` to a runnable form for pampy"""
    if isinstance(self.when, tuple):
      if len(self.when) == 0 or len(self.when) == 1:
        return self.when, self.then
      elif len(self.when) == 2:
        return self.when, lambda a, b: cast(Func1[Tuple[Any, Any], Any], self.then)((a, b))
      elif len(self.when) == 3:
        return self.when, lambda a, b, c: cast(Func1[Tuple[Any, Any, Any], Any], self.then)(
          (a, b, c))
      else:
        raise ValueError(f"Unacceptable Tuple length {len(self.when)}")
    else:
      return self.when, self.then

  def and_then(self, f: Func1[S, U]) -> "Case[T, U]":
    """map the Case's `then` result with f"""
    return Case(self.when, lambda a: f(self.then(a)))

  @staticmethod
  def v(when: Any, then: S) -> "Case[Any, S]":
    """Constructs a Case which returns just a value not executing function"""
    return Case(when, lambda _: then)


EndoCase = Case[T, T]


@dataclass(frozen=True)
class PartialFunc(Func1[T, S]):
  """
  Partial function wrapping pampy

  Examples:
    An example corresponding to pampy's one

    >>> from pampy import _
    >>> PartialFunc.cs(
    ...    Case.v(3, "this matches the number 3"),
    ...    Case.v(int, "matches any integer"),
    ...    Case((str, int), lambda t: f"a tuple ({t[0]}, {t[1]}) you can use in a function"),
    ...    Case.v([1, 2, _], "any list of 3 elements that begins with [1, 2]"),
    ...    Case.v({"x": _}, "any dict with a key 'x' and any value associated"),
    ...    Case.v(_, "anything else")).run(4)
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
    return PartialFunc([c.and_then(f) for c in self.cases])

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

  def __cases(self) -> List[Union[Func1[T, S], T]]:
    return [e for c in self.cases for e in c.to_runnable]

  def __whens(self) -> List[T]:
    return [c.when for c in self.cases]
