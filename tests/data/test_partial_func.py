from pampy import MatchError
from pytest import raises

from tats.data.Option import Some, Nothing
from tats.data.PartialFunc import Case, PartialFunc, EndoCase


class TestCase:
  def test_to_tuple(self):
    f = lambda a: a
    assert EndoCase(int, f).to_runnable == (int, f)

  def test_and_then(self):
    assert Case.v(str, "a").and_then(lambda s: s + "b").then("asdf") == "ab"
    assert EndoCase(str, lambda _: "a").and_then(lambda s: s + "b").then("") == "ab"

  def test_v(self):
    assert Case.v(str, "a").then("a") == Case(str, lambda _: "a").then("b")


class TestPartialFunc:
  def test_run(self):
    p = PartialFunc.cs(EndoCase(str, lambda s: s + "b"), EndoCase(int, lambda i: i + 1))
    assert p.run("a") == "ab"
    assert p.run(1) == 2
    with raises(MatchError):
      p.run(None)

  def test_is_defined_at(self):
    p = PartialFunc.cs(EndoCase(str, lambda s: s + "b"), EndoCase(int, lambda i: i + 1))
    assert p.is_defined_at(1)
    assert p.is_defined_at("a")
    assert not p.is_defined_at(None)

  def test_or_else(self):
    p1 = PartialFunc.cs(EndoCase(str, lambda s: s + "b"))
    p2 = PartialFunc.cs(Case[int, str](int, lambda i: str(i)))
    p3 = p1.or_else(p2)
    assert p3.run("a") == "ab"
    assert p3.run(1) == "1"

  def test_and_then(self):
    assert PartialFunc.cs(EndoCase(str, lambda s: s + "b"))\
             .and_then(lambda s: s + "c").run("a") == "abc"

  def test_lift(self):
    f = PartialFunc.cs(EndoCase(str, lambda s: s + "b")).lift
    assert f("a") == Some("ab")
    assert f(0) == Nothing()

  def test_run_or_else(self):
    f = PartialFunc.cs(EndoCase("a", lambda s: s + "b"))
    assert f.run_or_else("a", lambda s: s + "c") == "ab"
    assert f.run_or_else("a", lambda s: s + "c") == "ab"
