from pytest import raises

from tats.data.TList import TList


class TestTList:

  def test_head(self):
    assert TList([1, 2]).head == 1
    with raises(ValueError):
      TList([]).head

  def test_tail(self):
    assert TList([1, 2, 3]).tail == TList([2, 3])
    with raises(ValueError):
      TList([]).tail

  def test_take(self):
    assert TList([1, 2, 3]).take(2) == TList([1, 2])
    assert TList([1, 2, 3]).take(10) == TList([1, 2, 3])
    assert TList([1, 2, 3]).take(-1) == TList([])
    assert TList([1, 2, 3]).take(0) == TList([])

  def test_var(self):
    assert TList.var(1, 2) == TList([1, 2])

  def test_syntax(self):
    assert TList([1, 2, 3]).eqv(TList([1, 2, 3]))
    assert TList([1, 2, 3]).neqv(TList([1, 2]))
    assert TList([1, 2]).map(lambda x: x * 2) == TList([2, 4])
    assert TList([1, 2]).product_r(TList([3, 4])) == TList([3, 4, 3, 4])
    assert TList([1, 2]).product_l(TList([3, 4])) == TList([1, 1, 2, 2])
    assert TList([1, 2]).flat_map(lambda x: TList([x, x * 2])) == TList(
        [1, 2, 2, 4])
    assert TList([1, 2]).combine(TList([3, 4])) == TList([1, 2, 3, 4])
    assert TList([1, 2]) + TList([3, 4]) == TList([1, 2, 3, 4])
    assert TList([]).is_empty
    assert not TList([1, 2]).is_empty
