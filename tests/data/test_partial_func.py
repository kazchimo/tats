from typing import Any

from pampy import MatchError
from pytest import raises

from tats.data.PartialFunc import Case, PartialFunc


class TestCase:
  def test_to_tuple(self):
    f = lambda a: a
    assert Case(int, f).to_tuple == (int, f)


class TestPartialFunc:
  def test_run(self):
    p = PartialFunc.cs(Case[Any, Any](str, lambda s: s + "b"), Case[Any, Any](int, lambda i: i + 1))
    assert p.run("a") == "ab"
    assert p.run(1) == 2
    with raises(MatchError):
      p.run(None)
