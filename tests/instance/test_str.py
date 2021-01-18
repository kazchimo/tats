from tats.instance.str import StrInstance


class TestStrInstance:
  def test_combine(self):
    assert StrInstance().combine("a", "b") == "ab"

  def test_empty(self):
    assert StrInstance().empty == ""

  def test_reverse(self):
    assert StrInstance().reverse().combine("a", "b") == "ba"
