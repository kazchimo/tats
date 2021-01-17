from typing import TypeVar, Protocol, Callable

Arg = TypeVar("Arg", contravariant=True)
Res = TypeVar("Res", covariant=True)
T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")


class Func1(Protocol[Arg, Res]):

  def __call__(self, a: Arg) -> Res:
    ...


class BiOp(Protocol[Arg, Res]):

  def __call__(self, a: Arg, b: Arg) -> Res:
    ...


class EndoBiOp(Protocol[T]):

  def __call__(self, a: T, b: T) -> T:
    ...
