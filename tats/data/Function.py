from typing import TypeVar, Protocol, Generic, Callable, runtime_checkable

Arg1 = TypeVar("Arg1", contravariant=True)
Arg2 = TypeVar("Arg2", contravariant=True)
Arg3 = TypeVar("Arg3", contravariant=True)
Res = TypeVar("Res", covariant=True)
T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")


@runtime_checkable
class Func1(Protocol[Arg1, Res]):
  def __call__(self, a: Arg1) -> Res:
    ...


class Func1F(Generic[Arg1, Res]):
  """
  Factory of Func1
  """
  @staticmethod
  def true() -> Func1[Arg1, bool]:
    return lambda _: True

  @staticmethod
  def false() -> Func1[Arg1, bool]:
    return lambda _: False

  @staticmethod
  def id() -> Func1[T, T]:
    return lambda x: x

  @staticmethod
  def eq(e: Arg1) -> Func1[Arg1, bool]:
    return lambda x: x == e

  @staticmethod
  def const(a: A) -> Func1[Arg1, A]:
    return lambda _: a


@runtime_checkable
class Func2(Protocol[Arg1, Arg2, Res]):
  def __call__(self, a: Arg1, b: Arg2) -> Res:
    ...


EndoFunc2 = Func2[T, T, T]

BiOp = Func2[A, A, B]

EndoBiOp = Func2[A, A, A]


@runtime_checkable
class Func3(Protocol[Arg1, Arg2, Arg3, Res]):
  def __call__(self, a: Arg1, b: Arg2, c: Arg3) -> Res:
    ...
