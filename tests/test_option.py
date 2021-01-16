from tats.Option import Some, Nothing, OptionInstance


class TestOption:

  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()

  def test_non_empty(self):
    assert Some("").non_empty()
    assert not Nothing().non_empty()

  def test_or_else(self):
    assert Some(1).or_else(Some(2)) == Some(1)
    assert Nothing().or_else(Some(2)) == Some(2)
    assert Some(1).or_else(Nothing()) == Some(1)
    assert Nothing().or_else(Nothing()) == Nothing()

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

    assert Some(1).product_l(Some(2)) == Some(1)
    assert Nothing().product_l(Some(2)) == Nothing()
    assert Some(1).product_l(Nothing()) == Nothing()
    assert Nothing().product_l(Nothing()) == Nothing()
