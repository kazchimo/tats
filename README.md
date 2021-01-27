# tats
Type classes, Functional Data Types experimental implementations for Python inspired by Scala language design.

## Features
- Functional Data Types like Option, Either
- Type Classes and syntax derivation

## Examples
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
