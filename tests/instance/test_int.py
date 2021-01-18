from tats.instance.int import IntInstance


class TestIntInstance:
  def test_combine(self):
    assert IntInstance().combine(1, 2) == 3

  def test_empty(self):
    assert IntInstance().empty == 0
