## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* [Example 2: Using a Cluster](./Example2.md)
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* Example 4: Using Aliases
* [Example 5: Using Error Handlers](./Example5.md)
* [Example 6: Halting the Parser](./Example6.md)
* [Example 7: Printing Usage](./Example7.md)

----
### Example 4 : Using Aliases
#### Usage: 
    python test.py --exec-with 'Main File.sh'

    -- or --

    python test.py -exec 'Main File.sh'
#### Output:
    {'exec': 'Main File.sh'}
#### Code:
```python
import sys
from parameterparser import Cluster, Parameter, Parser

# Initialize the Cluster
parameters = Cluster()

# Create the Parameter
exec_parameter = Parameter("-", "exec", lambda file: file)

# Add an alias to the exec Parameter using prefix '--'
# and parameter alias 'exec-with'.
#
# Note: Aliases will always override regular parameters no
# matter what order they are added in. Aliases take precedence.
#
# Note: You can also define aliases with no prefix and the
# alias will use it's parent parameter's prefix.
exec_parameter.add_alias("exec-with", "--")

# Add the Parameter to the Cluster
parameters.add(exec_parameter)

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv, parameters)

# Parse the arguments using the Cluster.
results = parser.parse()

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid():
    parameters.print_full_usage(
        "Parameter Parser", 
        "Using aliases with Parameter Example.", 
        "v0.0.1"
    )
else:
    print(results)
```