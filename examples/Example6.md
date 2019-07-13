## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* [Example 2: Using a Cluster](./Example2.md)
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* [Example 4: Using Aliases](./Example4.md)
* [Example 5: Using Error Handlers](./Example5.md)
* Example 6: Halting the Parser
* [Example 7: Printing Usage](./Example7.md)

----
### Example 6 : Halting the Parser

#### Usage: 
    python test.py -load Test -exec 'some code'
#### Output: 
    Halted by: load
    {'load': 'Test'}
#### Code:
```python
import sys
from parameterparser import Cluster, Parameter, Parser, Result

# Define the handler for the load Parameter
def load_handler(name):
    # This will return a value for the parameter and
    # will then halt the Parser.
    return Result.halt(name)

    # This will return no value for the parameter and
    # then will halt the parser.
    # return Result.halt()

    # This will simply return the value for the parameter.
    # return name


# Initialize the Cluster
parameters = Cluster()

# Create the Parameter
load_parameter = Parameter("-", "load", load_handler)
exec_parameter = Parameter("-", "exec", lambda code: code)

# Add the Parameter to the Cluster
parameters.add_many([load_parameter, exec_parameter])

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv, parameters)

# Parse the arguments using the Cluster.
results = parser.parse()

# Check if the parser has been halted.
if parser.halted_by is not None:
    print("Halted by: " + parser.halted_by.name)

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid():
    parameters.print_full_usage(
        "Parameter Parser",
        "Halting the Parser.",
        "v0.0.1"
    )
else:
    print(results)
```
