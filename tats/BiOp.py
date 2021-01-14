from typing import TypeVar, Protocol

_T = TypeVar("_T")
_S = TypeVar("_S")


class BiOp(Protocol[_T, _S]):
  def __call__(self, a: _T, b: _T) -> _S:
    ...

class EndoBiOp(Protocol[_T]):
  def __call__(self, a: _T, b: _T) -> _T:
    ...

