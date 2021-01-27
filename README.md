# tats
Type classes, Functional Data Types experimental implementations for Python inspired by Scala language design.

## Features
- Functional Data Types like Option, Either
- Type Classes and syntax derivation

## Data Types
### Option
```python
from tats.data.Option import *

Option.from_nullable(None)
# => Nothing() 

Option.from_nullable(1)
# => Some(1)

## map the value
Some(1).map(lambda a: a * 2)
# => Some(2)

Nothing().map(lambda a: a * 2)
# => Nothing()

## flat_map
Some(1).flat_map(
  lambda a: Some(a * 2)
).flat_map(
  lambda a: Some(a * 2)
)
# => Some(4)
```

### PartialFunction
```python
from pampy import _
from tats.data.PartialFunc import *

PartialFunc.cs(
   Case.v(3, "this matches the number 3"),
   Case.v(int, "matches any integer"),
   Case((str, int), lambda t: f"a tuple ({t[0]}, {t[1]}) you can use in a function"),
   Case.v([1, 2, _], "any list of 3 elements that begins with [1, 2]"),
   Case.v({"x": _}, "any dict with a key 'x' and any value associated"),
   Case.v(_, "anything else")
).run(4)
# => "matches any integer"

from tats.data.Option import Nothing, Some

p = PartialFunc.cs(
  Case.v(Some(_), "some"),
  Case.v(Nothing(), "none")
)

p.run(Some(3)) # => "some"
p.run(Nothing()) # => "none"
```

## Type Classes
tats provides some type classses and convenient syntax mixins.
Type class instances should be passed explicitly if needed because Python has no builtin syntax to provide instances corresponding to Scala or Haskell's one.

```python
from tats.data.TList import *
from tats.data.Option import *
from tats.instance.option import *

# Semigroup syntax
TList.var(1, 2, 3).combine(TList.var(4, 5)) # => TList([1, 2, 3, 4, 5])

# Functor syntax
TList.var(1, 2).map(lambda a: a * 2) # => TList([2, 4])

# Monad syntax
TList.var(1, 2).flat_map(lambda a: TList.var(a, a + 1)) # => TList([1, 2, 2, 3])

# Applicative Syntax
Some(1).product_r(Some(2)) # => Some(2)

# year and you always need Traverse
TList.var(1, 2, 3).traverse(OptionInstance(), Some) # => Some(TList([1, 2, 3]))
TList.var(Some(1), Some(2), Some(3)).sequence(OptionInstance()) # => Some(TList([1, 2, 3]))
```
