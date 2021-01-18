from tats.Monoid import Monoid


class IntInstance(Monoid[int]):
  @staticmethod
  def _cmb(a: int, b: int) -> int:
    return a + b

  @property
  def empty(self) -> int:
    return 0
