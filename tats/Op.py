from typing import TypeVar, Protocol, Type

Arg = TypeVar("Arg", contravariant=True)
Res = TypeVar("Res", covariant=True)
T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")


class UnOp(Protocol[Arg, Res]):

  def __call__(self, a: Arg) -> Res:
    ...


def unop_typed(f: "UnOp[A, B]", a: Type[A], r: Type[B]) -> "UnOp[A, B]":
  return f


class BiOp(Protocol[Arg, Res]):

  def __call__(self, a: Arg, b: Arg) -> Res:
    ...


class EndoBiOp(Protocol[T]):

  def __call__(self, a: T, b: T) -> T:
    ...
