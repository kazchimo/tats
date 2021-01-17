from pytest import raises

from tats.data.Either import Left, Right


class TestEither:

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

    def _raise():
      raise Exception

    with raises(Exception):
      Right(1).foreach(_raise)

    Left(1).foreach(_raise)

  def test_get_or_else(self):
    assert Right(1).get_or_else(2) == 1
    assert Left(1).get_or_else(2) == 2

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
