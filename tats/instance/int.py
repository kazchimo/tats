from tats.Monoid import Monoid


class IntInstance(Monoid[int]):
  @staticmethod
  def combine(a: int, b: int) -> int:
    return a + b

  @staticmethod
  def empty() -> int:
    return 0
