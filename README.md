# tats
Type classes, Functional Data Types experimental implementations for Python inspired by Scala language design.

## Features
- Functional Data Types like Option, Either
- Type Classes and syntax derivation

## Examples
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
```
