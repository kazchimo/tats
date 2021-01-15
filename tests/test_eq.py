from tats.Eq import Eq


class TestEq:
  def test_instance(self):
    StrEq: Eq[str] = Eq(lambda a, b: a == b)
    assert StrEq.eqv("a", "a")
    assert StrEq.neqv("a", "b")

