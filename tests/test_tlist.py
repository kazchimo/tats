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

  def test_drop(self):
    assert TList([1, 2, 3]).drop(2) == TList([3])
    assert TList([1, 2, 3]).drop(10) == TList([])
    assert TList([1, 2, 3]).drop(-1) == TList([1, 2, 3])
    assert TList([1, 2, 3]).drop(0) == TList([1, 2, 3])

  def test_take_right(self):
    assert TList([1, 2, 3]).take_right(2) == TList([2, 3])
    assert TList([1, 2, 3]).take_right(10) == TList([1, 2, 3])
    assert TList([1, 2, 3]).take_right(-1) == TList([])
    assert TList([1, 2, 3]).take_right(0) == TList([])

  def test_split_at(self):
    assert TList([1, 2, 3]).split_at(2) == (TList([1, 2]), TList([3]))
    assert TList([1, 2, 3]).split_at(10) == (TList([1, 2, 3]), TList([]))
    assert TList([1, 2, 3]).split_at(-1) == (TList([]), TList([1, 2, 3]))
    assert TList([1, 2, 3]).split_at(0) == (TList([]), TList([1, 2, 3]))

  def test_take_while(self):
    assert TList([1, 2, 3]).take_while(lambda x: x < 3) == TList([1, 2])
    assert TList([1, 2, 3]).take_while(lambda x: x < 0) == TList([])
    assert TList([1, 2, 3]).take_while(lambda x: x < 4) == TList([1, 2, 3])

  def test_drop_while(self):
    assert TList([1, 2, 3]).drop_while(lambda x: x < 3) == TList([3])
    assert TList([1, 2, 3]).drop_while(lambda x: x < 0) == TList([1, 2, 3])
    assert TList([1, 2, 3]).drop_while(lambda x: x < 4) == TList([])

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
