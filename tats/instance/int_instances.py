from tats.Semigroup import Semigroup


class IntInstance(Semigroup[int]):

  @staticmethod
  def _cmb(a: int, b: int) -> int:
    return a + b
