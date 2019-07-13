## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* [Example 2: Using a Cluster](./Example2.md)
* Example 3: Using a Cluster with Variadic Arguments (`*args`)
* [Example 4: Using Aliases](./Example4.md)
* [Example 5: Using Error Handlers](./Example5.md)
* [Example 6: Halting the Parser](./Example6.md)
* [Example 7: Printing Usage](./Example7.md)

----
### Example 3 : Using a Cluster with Variadic Arguments (`*args`)

> Note: Parameter Parser does not support `**kwargs` as there is no proper way to represent this in the command line succinctly. 

#### Usage: 
    python test.py -load 'Main Library.so' File2.so +configurewith 'Main Library.so' -exec 'Pre Load.sh' Initialize.sh start.sh
#### Output:
    {'load': ('Main Library.so', 'File2.so'), 'configurewith': 'Main Library.so', 'exec': ('Pre Load.sh', 'Initialize.sh', 'start.sh')}
#### Code:
```python
import sys
from parameterparser import Cluster, Parameter, Parser

# Define the handlers for each Parameter.
def load_handler(*files):
    return files


def exec_handler(*files):
    return files


def configurewith_handler(file):
    return file


# Initialize the Cluster
parameters = Cluster()

# Create each of the Parameters
load_parameter = Parameter("-", "load", load_handler)
exec_parameter = Parameter("-", "exec", exec_handler)
configurewith_parameter = Parameter("+", "configurewith", configurewith_handler)

# Add the Parameters to the Cluster
# You can use either .add_many() to add multiple Parameters at once
# or you can use .add() to add a single Parameter at a time.
parameters.add_many([load_parameter, exec_parameter, configurewith_parameter])

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv, parameters)

# Parse the arguments using the Cluster.
results = parser.parse()

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid():
    parameters.print_full_usage(
        "Parameter Parser", 
        "Using a Cluster with Variadic Arguments (*args)", 
        "v0.0.1"
    )
else:
    print(results)
```
