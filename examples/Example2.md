## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* Example 2: Using a Cluster
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* [Example 4: Using Aliases](./Example4.md)
* [Example 5: Using Error Handlers](./Example5.md)
* [Example 6: Halting the Parser](./Example6.md)
* [Example 7: Printing Usage](./Example7.md)

----
### Example 2 : Using a Cluster to parse more advanced parameters.

#### Usage: 
    python test.py -name "Nathan Fiscaletti" +minify --join 'foo bar' apples --invite 'Mr. Foo' 'Mr. Bar'
#### Output:
    {'name': 'Nathan Fiscaletti', 'minify': True, 'join': 'foo barapples', 'invite': ['Mr. Foo', 'Mr. Bar']}
#### Code:
```python
import sys
from parameterparser import Cluster, Parameter, Parser

# Define the handlers for each Parameter.
#
# Parameters accept a Callable for their handler.
# In this example we use both regular def functions
# as well as lambdas.


def name_handler(name):
    return name


def invite_handler(name1, name2):
    return [name1, name2]


def join_handler(first, second):
    return str(first) + str(second)


# Initialize the Cluster
parameters = Cluster()

# Create each of the Parameters
name_parameter = Parameter("-", "name", name_handler)
invite_parameter = Parameter("--", "invite", invite_handler)
join_parameter = Parameter("--", "join", join_handler)
minify_parameter = Parameter("+", "minify", lambda: True)

# Add the Parameters to the Cluster
# You can use either .add_many() to add multiple Parameters at once
# or you can use .add() to add a single Parameter at a time.
parameters.add_many([name_parameter, minify_parameter, invite_parameter, join_parameter])

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv, parameters)

# Parse the arguments using the Cluster.
results = parser.parse()

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid():
    parameters.print_full_usage(
        "Parameter Parser", 
        "Using ParameterCluster to parse more advanced parameters Example.", 
        "v0.0.1"
    )
else:
    print(results)
```
