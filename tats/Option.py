from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Optional, Any, Literal

from pampy import match, _
from returns.primitives.hkt import SupportsKind1

from .Functor import Functor
from .Op import UnOp

A = TypeVar("A")
B = TypeVar("B")
URI = Literal["Option"]


class Option(SupportsKind1[URI, A]):

  @abstractmethod
  def is_empty(self) -> bool:
    ...

  @staticmethod
  def pure(a: Optional[A]) -> "Option[A]":
    return Some(a) if a is not None else Nothing()


@dataclass(frozen=True)
class Some(Option[A]):
  a: A

  def is_empty(self) -> bool:
    return False


@dataclass()
class Nothing(Option[Any]):

  def is_empty(self) -> bool:
    return True


class OptionFunctor(Functor[URI]):

  @staticmethod
  def map(fa: SupportsKind1[URI, A], f: UnOp[A, B]) -> SupportsKind1[URI, B]:
    return match(\
      fa,
      Some(_), lambda x: Some(f(x)),
      Nothing, lambda x: Nothing())
