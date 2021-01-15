from tats.Option import Some, Nothing, Option


class TestOption:
  def test_call(self):
    assert Option.pure("a") == Some("a")
    assert Option.pure(None) == Nothing()

  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()
