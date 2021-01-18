from tats.Monoid import Monoid


class StrInstance(Monoid[str]):
  @property
  def empty(self) -> str:
    return ""

  def combine(self, a: str, b: str) -> str:
    return a + b
