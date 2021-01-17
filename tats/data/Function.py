from typing import TypeVar, Protocol, Generic

Arg = TypeVar("Arg", contravariant=True)
Res = TypeVar("Res", covariant=True)
T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")


class Func1(Protocol[Arg, Res]):

  def __call__(self, a: Arg) -> Res:
    ...


class Func1F(Generic[Arg, Res]):

  @staticmethod
  def true() -> Func1[Arg, bool]:
    return lambda _: True

  @staticmethod
  def false() -> Func1[Arg, bool]:
    return lambda _: False

  @staticmethod
  def id() -> Func1[Arg, Res]:
    return lambda x: x

  @staticmethod
  def eq(e: Arg) -> Func1[Arg, bool]:
    return lambda x: x == e

  @staticmethod
  def const(a: A) -> Func1[Arg, A]:
    return lambda _: a


class BiOp(Protocol[Arg, Res]):

  def __call__(self, a: Arg, b: Arg) -> Res:
    ...


class EndoBiOp(Protocol[T]):

  def __call__(self, a: T, b: T) -> T:
    ...
