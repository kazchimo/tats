from tats.Eq import Eq



class TestEq:

  def test_instance(self):
    StrEq: Eq[str] = Eq(lambda a, b: a == b)
    assert StrEq.eqv("a", "a")
    assert StrEq.neqv("a", "b")

  def test_contramap(self):
    IntEq: Eq[int] = Eq(lambda a, b: a == b)
    StrEq = IntEq.contramap(len)
    assert StrEq.eqv("ab", "ab")
    assert StrEq.neqv("ab", "a")

