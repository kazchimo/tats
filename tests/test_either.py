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

    assert Right(Right(1)).flatten() == Right(1)
    assert Right(Left(1)).flatten() == Left(1)
    assert Left(1).flatten() == Left(1)

    assert Right(1).flat_map(lambda x: Right(x + 1)) == Right(2)
    assert Left(1).flat_map(lambda x: Right(x + 1)) == Left(1)
    assert Right(1).flat_map(lambda x: Left("a")) == Left("a")
    assert Left(1).flat_map(lambda x: Left("a")) == Left(1)