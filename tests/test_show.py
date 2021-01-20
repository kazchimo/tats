from tats.Show import Show


class TestShow:
  def test_instance(self):
    intShow: Show[int] = Show.instance(lambda i: f"int is {i}")
    assert intShow.show(1) == "int is 1"
