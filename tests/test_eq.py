from typing import Type

from tats.Eq import Eq


class TestEq:
  def test_instance(self):
    StrEq: Type[Eq[str]] = Eq.instance("StrEq", lambda a, b: a == b)
    assert StrEq.eqv("a", "a")
    assert StrEq.neqv("a", "b")

