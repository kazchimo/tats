from pytest import raises

from tats.data.PartialFunc import PartialFunc, Case
from tats.data.Option import Some, Nothing
from tats.data.TList import TList
from tats.instance.option import OptionInstance


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

  def test_split(self):
    assert TList([1, 2, 3]).span(lambda x: x < 3) == (TList([1, 2]), TList([3]))
    assert TList([1, 2, 3])\
             .span(lambda x: x < 0) == (TList([]), TList([1, 2, 3]))
    assert TList([1, 2, 3]).span(lambda x: x < 4) == (TList([1, 2, 3]), TList([]))

  def test_var(self):
    assert TList.var(1, 2) == TList([1, 2])

  def test_get_item(self):
    assert TList.var(1, 2)[0] == 1
    assert TList.var(1, 2, 3, 4)[2:3] == TList.var(3)
    assert TList.var(1, 2, 3, 4)[2:] == TList.var(3, 4)
    assert TList.var(1, 2, 3, 4)[:3] == TList.var(1, 2, 3)
    assert TList.var(1, 2, 3, 4)[:-1] == TList.var(1, 2, 3)
    assert TList.var(1, 2, 3, 4)[::-1] == TList.var(1, 2, 3, 4).reverse

  def test_iter(self):
    assert [i for i in TList.var(1, 2, 3)] == [1, 2, 3]

  def test_size(self):
    assert TList.var(1, 2, 3).size == 3

  def test_len(self):
    assert len(TList.var(1, 2, 3)) == 3

  def test_syntax(self):
    assert TList([1, 2, 3]).eqv(TList([1, 2, 3]))
    assert TList([1, 2, 3]).neqv(TList([1, 2]))
    assert TList([1, 2]).map(lambda x: x * 2) == TList([2, 4])
    assert TList([1, 2]).product_r(TList([3, 4])) == TList([3, 4, 3, 4])
    assert TList([1, 2]).product_l(TList([3, 4])) == TList([1, 1, 2, 2])
    assert TList([1, 2]).flat_map(lambda x: TList([x, x * 2])) == TList([1, 2, 2, 4])
    assert TList([1, 2]).combine(TList([3, 4])) == TList([1, 2, 3, 4])
    assert TList([1, 2]) + TList([3, 4]) == TList([1, 2, 3, 4])
    assert TList([1, 2]) + TList([3, 4]) == TList([1, 2, 3, 4])
    assert TList([]).is_empty
    assert not TList([1, 2]).is_empty
    assert TList([1, 2, 3]).fold_left(0, lambda a, b: a + b) == 6
    assert TList([1, 2, 3]).reduce_left_to_option(str, lambda a, b: a + str(b)) == Some("123")
    assert TList([]).reduce_left_to_option(str, lambda a, b: a + str(b)) == Nothing()
    assert TList([1, 2, 3]).reduce_left_option(lambda a, b: a + b) == Some(6)
    assert TList([]).reduce_left_option(lambda a, b: a + b) == Nothing()
    assert TList([1, 2, 3]).to_tlist() == TList([1, 2, 3])
    assert TList([1, 2, 3]).map2(TList([4, 5]), lambda a, b: a * b) == TList([4, 5, 8, 10, 12, 15])
    assert TList([1, 2, 3]).product(TList([4, 5 ])) ==\
           TList([(1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)])
    assert TList([1, 2, 3]).traverse(OptionInstance(), Some) == Some(TList([1, 2, 3]))
    assert TList([1, 2, 3])\
             .traverse(OptionInstance(), lambda x: Nothing() if x > 2 else Some(x)) == Nothing()
    assert TList([Some(1), Some(2), Some(3)]).sequence(OptionInstance()) == Some(TList([1, 2, 3]))
    assert TList([Some(1), Nothing(), Some(3)]).sequence(OptionInstance()) == Nothing()
    assert TList([1, 2, 3]).flat_traverse(OptionInstance(), lambda x: Some(TList([x, x + 1]))) == \
           Some(TList([1, 2, 2, 3, 3, 4]))
    assert TList([1, 2, 3]).flat_traverse(
      OptionInstance(), lambda x: Some(TList([x, x + 1])) if x < 2 else Nothing()) == Nothing()

    assert TList.var(1, 2, 3).map_filter(lambda a: Some(a) if a < 3 else Nothing()) == \
           TList.var(1, 2)
    assert TList.var(1, 2, 3).collect(PartialFunc.cs(Case.v(1, "a"), Case.v(2, "b"))) == \
           TList.var("a", "b")
    assert TList.var(1, 2, 3).filter(lambda a: a < 3) == TList.var(1, 2)
    assert TList.var(1, 2, 3).filter_not(lambda a: a < 3) == TList.var(3)
