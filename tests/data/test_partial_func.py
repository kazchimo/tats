from typing import Any

from pampy import MatchError
from pytest import raises

from tats.data.PartialFunc import Case, PartialFunc


class TestCase:
  def test_to_tuple(self):
    f = lambda a: a
    assert Case(int, f).to_tuple == (int, f)

  def test_map(self):
    assert Case(str, "a").map(lambda s: s + "b") == Case(str, "ab")
    assert Case(str, lambda _: "a").map(lambda s: s + "b").then("") == "ab"


class TestPartialFunc:
  def test_run(self):
    p = PartialFunc.cs(Case[Any, Any](str, lambda s: s + "b"), Case[Any, Any](int, lambda i: i + 1))
    assert p.run("a") == "ab"
    assert p.run(1) == 2
    with raises(MatchError):
      p.run(None)

  def test_is_defined_at(self):
    p = PartialFunc.cs(Case[Any, Any](str, lambda s: s + "b"), Case[Any, Any](int, lambda i: i + 1))
    assert p.is_defined_at(1)
    assert p.is_defined_at("a")
    assert not p.is_defined_at(None)

  def test_or_else(self):
    p1 = PartialFunc.cs(Case(str, lambda s: s + "b"))
    p2 = PartialFunc.cs(Case(int, lambda i: i + 1))
    p3 = p1.or_else(p2)
    assert p3.run("a") == "ab"
    assert p3.run(1) == 2

  def test_and_then(self):
    assert PartialFunc.cs(Case(str, lambda s: s + "b"))\
             .and_then(lambda s: s + "c").run("a") == "abc"
