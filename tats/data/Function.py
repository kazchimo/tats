from typing import TypeVar, Protocol, Generic

Arg1 = TypeVar("Arg1", contravariant=True)
Arg2 = TypeVar("Arg2", contravariant=True)
Arg3 = TypeVar("Arg3", contravariant=True)
Res = TypeVar("Res", covariant=True)
T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")


class Func1(Protocol[Arg1, Res]):
  def __call__(self, a: Arg1) -> Res:
    ...


class Func1F(Generic[Arg1, Res]):
  @staticmethod
  def true() -> Func1[Arg1, bool]:
    return lambda _: True

  @staticmethod
  def false() -> Func1[Arg1, bool]:
    return lambda _: False

  @staticmethod
  def id() -> Func1[Arg1, Res]:
    return lambda x: x

  @staticmethod
  def eq(e: Arg1) -> Func1[Arg1, bool]:
    return lambda x: x == e

  @staticmethod
  def const(a: A) -> Func1[Arg1, A]:
    return lambda _: a


class Func2(Protocol[Arg1, Arg2, Res]):
  def __call__(self, a: Arg1, b: Arg2) -> Res:
    ...


class Func3(Protocol[Arg1, Arg2, Arg3, Res]):
  def __call__(self, a: Arg1, b: Arg2, c: Arg3) -> Res:
    ...


class BiOp(Protocol[Arg1, Res]):
  def __call__(self, a: Arg1, b: Arg1) -> Res:
    ...


class EndoBiOp(Protocol[T]):
  def __call__(self, a: T, b: T) -> T:
    ...
