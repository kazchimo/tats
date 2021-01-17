from tats.Semigroup import Semigroup


class IntSemigroup(Semigroup[int]):

  @staticmethod
  def _cmb(a: int, b: int) -> int:
    return a + b
