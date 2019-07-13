## Index:
* Example 1: Using Parameter Parser
* [Example 2: Using a Cluster](./Example2.md)
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* [Example 4: Using Aliases](./Example4.md)
* [Example 5: Using Error Handlers](./Example5.md)
* [Example 6: Halting the Parser](./Example6.md)
* [Example 7: Printing Usage](./Example7.md)

----
### Example 1 : Using Parameter Parser to parse simple parameters.

#### Usage: 
    python test.py silent color
#### Output: 
    {'silent': True, 'color': True}
#### Code:
```python
import sys
from parameterparser import Parser

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv)

# Set the default handler for the parser.
# In this example, we will just have two parameters that can be set.
#
# Always return -1 if no valid parameter is found. This will
# invalidate the parser.
#
# After calling parser.parse(), user parser.is_valid() to check
# the validity of the parser.
#
# By default, if no parameter is found in the parser and no
# default has been set, -1 will be returned.
parser.set_default(
    lambda parameter:
        True if
        parameter == "silent" or parameter == "color"
        else -1
)

# Parse the arguments using the Parameter Parser.
results = parser.parse()

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid():
    print("Usage: python __init.py__ [color] [silent]")
else:
    print(results)
```
