from tats.Option import Some, Nothing, Option, OptionInstance


class TestOption:

  def test_call(self):
    assert Option.pure("a") == Some("a")
    assert Option.pure(None) == Nothing()

  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()

  def test_functor(self):
    OptionInstance.map(Some(1), lambda x: x * 2) == Some(2)
    OptionInstance.map(Nothing(), lambda x: x * 2) == Nothing()

  def test_apply(self):
    assert OptionInstance.ap(Some(lambda x: x * 2), Some(1)) == Some(2)
    assert OptionInstance.ap(Nothing(), Some(1)) == Nothing()
    assert OptionInstance.ap(Some(lambda x: x * 2), Nothing()) == Nothing()
    assert OptionInstance.ap(Nothing(), Nothing()) == Nothing()

  def test_syntax(self):
    assert Some(1).map(lambda x: x * 2) == Some(2)
    assert Nothing().map(lambda x: x * 2) == Nothing()

    assert Some(1).product_r(Some(2)) == Some(2)
    assert Nothing().product_r(Some(2)) == Nothing()
    assert Some(1).product_r(Nothing()) == Nothing()
    assert Nothing().product_r(Nothing()) == Nothing()
