from tats.Eq import Eq


class TestEq:
  def test_init(self):
    StrEq: Eq[str] = Eq.instance(lambda a, b: a == b)
    assert StrEq.eqv("a", "a")
    assert StrEq.neqv("a", "b")

  def test_contramap(self):
    IntEq: Eq[int] = Eq.instance(lambda a, b: a == b)
    StrEq: Eq[str] = IntEq.contramap(lambda x: len(x))
    assert StrEq.eqv("ab", "ab")
    assert StrEq.neqv("ab", "a")

  def test_and(self):
    HeadEq: Eq[str] = Eq.instance(lambda a, b: a[0] == b[0])
    TailEq: Eq[str] = Eq.instance(lambda a, b: a[-1] == b[-1])
    HeadTailEq = HeadEq.and_(TailEq)
    assert HeadTailEq.eqv("abc", "aac")
    assert HeadTailEq.neqv("abc", "abb")
