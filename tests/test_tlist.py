from tats.data.TList import TList


class TestTList:

  def test_var(self):
    assert TList.var(1, 2) == TList([1, 2])

  def test_syntax(self):
    assert TList([1, 2, 3]).eqv(TList([1, 2, 3]))
    assert TList([1, 2, 3]).neqv(TList([1, 2]))

    assert TList([1, 2]).map(lambda x: x * 2) == TList([2, 4])

    assert TList([1, 2]).product_r(TList([3, 4])) == TList([3, 4, 3, 4])

    assert TList([1, 2]).product_l(TList([3, 4])) == TList([1, 1, 2, 2])

    assert TList([1, 2]).flat_map(lambda x: [x, x * 2]) == TList([1, 2, 2, 4])