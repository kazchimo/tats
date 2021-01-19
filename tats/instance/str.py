from tats.Monoid import Monoid


class StrInstance(Monoid[str]):
  @staticmethod
  def empty() -> str:
    return ""

  @staticmethod
  def combine(a: str, b: str) -> str:
    return a + b
