from pytest import raises

from tats.instance.int_instances import IntSemigroup
from tats.data.Either import Right, Left
from tats.data.Option import Some, Nothing, OptionInstance, Option


class TestOption:

  def test_from_nullable(self):
    assert Option.from_nullable(1) == Some(1)
    assert Option.from_nullable(None) == Nothing()

  def test_when(self):
    assert Option.when(True, 1) == Some(1)
    assert Option.when(False, 1) == Nothing()

  def test_unless(self):
    assert Option.unless(True, 1) == Nothing()
    assert Option.unless(False, 1) == Some(1)

  def test_is_empty(self):
    assert not Some("").is_empty()
    assert Nothing().is_empty()

  def test_non_empty(self):
    assert Some("").non_empty()
    assert not Nothing().non_empty()

  def test_or_else(self):
    assert Some(1).or_else(Some(2)) == Some(1)
    assert Nothing().or_else(Some(2)) == Some(2)
    assert Some(1).or_else(Nothing()) == Some(1)
    assert Nothing().or_else(Nothing()) == Nothing()

  def test_get(self):
    assert Some(1).get == 1
    with raises(ValueError):
      Nothing().get

  def test_get_or_else(self):
    assert Some(1).get_or_else(2) == 1
    assert Nothing().get_or_else(2) == 2

  def test_fold(self):
    assert Some(1).fold("a", str) == "1"
    assert Nothing().fold("a", str) == "a"

  def test_filter(self):
    assert Some(1).filter(lambda x: x == 1) == Some(1)
    assert Some(1).filter(lambda x: x == 2) == Nothing()
    assert Nothing().filter(lambda x: x == 2) == Nothing()

  def test_filter_not(self):
    assert Some(1).filter_not(lambda x: x == 1) == Nothing()
    assert Some(1).filter_not(lambda x: x == 2) == Some(1)
    assert Nothing().filter_not(lambda x: x == 2) == Nothing()

  def test_foreach(self):

    def _raise(_):
      raise Exception

    with raises(Exception):
      Some(1).foreach(_raise)

    Nothing().foreach(_raise)

  def test_with_filter(self):
    assert Some(1).with_filter(lambda x: x == 1).map(lambda x: x * 2) == Some(2)
    assert Nothing()\
             .with_filter(lambda x: x == 1)\
             .map(lambda x: x * 2) == Nothing()
    assert Some(1)\
             .with_filter(lambda x: x == 2)\
             .map(lambda x: x * 2) == Nothing()

    assert Some(1)\
             .with_filter(lambda x: x == 1)\
             .flat_map(lambda x: Some(x * 2)) == Some(2)
    assert Nothing()\
             .with_filter(lambda x: x == 1)\
             .flat_map(lambda x: Some(x * 2)) == Nothing()
    assert Some(1) \
             .with_filter(lambda x: x == 2) \
             .flat_map(lambda x: Some(x * 2)) == Nothing()

    def _raise(_):
      raise Exception

    with raises(Exception):
      Some(1) \
               .with_filter(lambda x: x == 1) \
               .foreach(_raise)
    Nothing() \
             .with_filter(lambda x: x == 1) \
             .foreach(_raise)
    Some(1) \
             .with_filter(lambda x: x == 2) \
             .foreach(_raise)

    assert Some(1)\
             .with_filter(lambda x: x == 1)\
             .with_filter(lambda x: x % 2 == 1)\
             .map(lambda x: x * 2) == Some(2)
    assert Nothing() \
             .with_filter(lambda x: x == 1) \
             .with_filter(lambda x: x % 2 == 1) \
             .map(lambda x: x * 2) == Nothing()
    assert Some(1) \
             .with_filter(lambda x: x == 2) \
             .with_filter(lambda x: x % 2 == 1) \
             .map(lambda x: x * 2) == Nothing()

  def test_contains(self):
    assert Some(1).contains(1)
    assert not Nothing().contains(1)

  def test_exists(self):
    assert Some(1).exists(lambda x: x == 1)
    assert not Some(1).exists(lambda x: x == 2)
    assert not Nothing().exists(lambda x: x == 1)

  def test_forall(self):
    assert Some(1).forall(lambda x: x == 1)
    assert not Some(1).forall(lambda x: x == 2)
    assert Nothing().forall(lambda x: x == 1)

  def test_to_right(self):
    assert Some(1).to_right("a") == Right(1)
    assert Nothing().to_right("a") == Left("a")

  def test_to_left(self):
    assert Some(1).to_left("a") == Left(1)
    assert Nothing().to_left("a") == Right("a")

  def test_eq(self):
    assert Some(1).eqv(Some(1))
    assert not Some(1).eqv(Some(2))
    assert Some(1).neqv(Nothing())
    assert Nothing().neqv(Some(1))
    assert Nothing().eqv(Nothing())

  def test_functor(self):
    OptionInstance.map(Some(1), lambda x: x * 2) == Some(2)
    OptionInstance.map(Nothing(), lambda x: x * 2) == Nothing()

  def test_apply(self):
    assert OptionInstance.ap(Some(lambda x: x * 2), Some(1)) == Some(2)
    assert OptionInstance.ap(Nothing(), Some(1)) == Nothing()
    assert OptionInstance.ap(Some(lambda x: x * 2), Nothing()) == Nothing()
    assert OptionInstance.ap(Nothing(), Nothing()) == Nothing()

  def test_syntax(self):
    assert Some(1).map(lambda x: x * 2) == Some(2)
    assert Nothing().map(lambda x: x * 2) == Nothing()

    assert Some(1).product_r(Some(2)) == Some(2)
    assert Nothing().product_r(Some(2)) == Nothing()
    assert Some(1).product_r(Nothing()) == Nothing()
    assert Nothing().product_r(Nothing()) == Nothing()

    assert Some(1).product_l(Some(2)) == Some(1)
    assert Nothing().product_l(Some(2)) == Nothing()
    assert Some(1).product_l(Nothing()) == Nothing()
    assert Nothing().product_l(Nothing()) == Nothing()

    assert Some(1).flat_map(lambda x: Some(x * 2)) == Some(2)
    assert Some(1).flat_map(lambda x: Nothing()) == Nothing()
    assert Nothing().flat_map(lambda x: Some(x * 2)) == Nothing()
    assert Nothing().flat_map(lambda x: Nothing()) == Nothing()

    assert Some(1).combine(IntSemigroup(), Some(1)) == Some(2)
    assert Nothing().combine(IntSemigroup(), Some(1)) == Nothing()
    assert Some(1).combine(IntSemigroup(), Nothing()) == Nothing()
    assert Nothing().combine(IntSemigroup(), Nothing()) == Nothing()
