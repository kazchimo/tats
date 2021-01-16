from tats.Option import Some, Nothing, Option, OptionFunctor


class TestOption:

  def test_call(self):
    assert Option.pure("a") == Some("a")
    assert Option.pure(None) == Nothing()

  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()

  def test_functor(self):
    OptionFunctor.map(Some(1), lambda x: x * 2) == Some(2)
    OptionFunctor.map(Nothing(), lambda x: x * 2) == Nothing()
