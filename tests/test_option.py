from tats.Option import Some, Nothing


class TestOption:
  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()
