from pytest import raises

from tats.data.TList import TList
from tats.instance.tlist import TListInstance
from tats.instance.int import IntInstance
from tats.data.Option import Some, Nothing
from tats.data.Either import Left, Right, Either


class TestEither:
  def test_cond(self):
    assert Either.cond(True, 1, 2) == Right(1)
    assert Either.cond(False, 1, 2) == Left(2)

  def test_is_left(self):
    assert Left(1).is_left()
    assert not Right(1).is_left()

  def test_is_right(self):
    assert not Left(1).is_right()
    assert Right(1).is_right()

  def test_fold(self):
    assert Left(1).fold(lambda l: l * 2, lambda r: r * 3) == 2
    assert Right(1).fold(lambda l: l * 2, lambda r: r * 3) == 3

  def test_swap(self):
    assert Right(1).swap == Left(1)
    assert Left(1).swap == Right(1)

  def test_foreach(self):
    def _raise(_):
      raise Exception

    with raises(Exception):
      Right(1).foreach(_raise)

    Left(1).foreach(_raise)

  def test_get(self):
    with raises(Exception):
      Left(1).get

    assert Right(1).get == 1

  def test_get_or_else(self):
    assert Right(1).get_or_else(2) == 1
    assert Left(1).get_or_else(2) == 2

  def test_or_else(self):
    assert Right(1).or_else(Right(2)) == Right(1)
    assert Left(1).or_else(Right(2)) == Right(2)

  def test_contains(self):
    assert Right(1).contains(1)
    assert not Right(1).contains(2)
    assert not Left(1).contains(1)

  def test_forall(self):
    assert Right(1).forall(lambda x: x == 1)
    assert not Right(1).forall(lambda x: x == 2)
    assert Left(1).forall(lambda x: x == 1)

  def test_exists(self):
    assert Right(1).exists(lambda x: x == 1)
    assert not Right(1).exists(lambda x: x == 2)
    assert not Left(1).exists(lambda x: x == 1)

  def test_to_option(self):
    assert Right(1).to_option() == Some(1)
    assert Left(1).to_option() == Nothing()

  def test_syntax(self):
    assert Left(1).map(lambda l: l * 2) == Left(1)
    assert Right(1).map(lambda l: l * 2) == Right(2)

    assert Right(1).product_r(Right(2)) == Right(2)
    assert Left(1).product_r(Right(2)) == Left(1)
    assert Right(1).product_r(Left(2)) == Left(2)
    assert Left(1).product_r(Left(2)) == Left(1)

    assert Right(1).product_l(Right(2)) == Right(1)
    assert Left(1).product_l(Right(2)) == Left(1)
    assert Right(1).product_l(Left(2)) == Left(2)
    assert Left(1).product_l(Left(2)) == Left(1)

    assert Right(1).flat_map(lambda x: Right(x + 1)) == Right(2)
    assert Left(1).flat_map(lambda x: Right(x + 1)) == Left(1)
    assert Right(1).flat_map(lambda x: Left("a")) == Left("a")
    assert Left(1).flat_map(lambda x: Left("a")) == Left(1)

    assert Right(1).eqv(Right(1))
    assert Right(1).neqv(Right(2))
    assert Right(1).neqv(Left(1))
    assert Left(1).eqv(Left(1))

    assert Right(1).combine(IntInstance(), Right(2)) == Right(3)
    assert Left(1).combine(IntInstance(), Right(2)) == Left(1)
    assert Right(1).combine(IntInstance(), Left(2)) == Left(2)
    assert Left(1).combine(IntInstance(), Left(2)) == Left(1)

    assert Right(1).traverse(TListInstance(), lambda a: TList([a, a * 2])) == \
           TList([Right(1), Right(2)])
    assert Left(1).traverse(TListInstance(), lambda a: TList([a, a * 2])) == \
      TList([Left(1)])
    assert Right(1).flat_traverse(TListInstance(), lambda a: TList([Right(a), Right(a * 2)])) == \
           TList([Right(1), Right(2)])
    assert Left(1).flat_traverse(TListInstance(), lambda a: TList([Right(a), Right(a * 2)])) == \
           TList([Left(1)])
    assert Right(1).flat_traverse(TListInstance(), lambda a: TList([Left(a), Right(a * 2)])) == \
           TList([Left(1), Right(2)])
    assert Right(TList.var(1, 2)).sequence(TListInstance()) == TList.var(Right(1), Right(2))
    assert Left(TList.var(1, 2)).sequence(TListInstance()) == \
           Left(TList.var(1, 2)).sequence(TListInstance())
