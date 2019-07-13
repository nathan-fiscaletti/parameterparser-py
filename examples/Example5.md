## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* [Example 2: Using a Cluster](./Example2.md)
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* [Example 4: Using Aliases](./Example4.md)
* Example 5: Using Error Handlers
* [Example 6: Halting the Parser](./Example6.md)
* [Example 7: Printing Usage](./Example7.md)

----
### Example 5 : Using Error Handlers

#### Usage: 
    python test.py -name
#### Output:
    ParseException: [60002] (parameter: name) : Invalid argument count. Expecting 1 but received 0.

    Parameter Parser v0.0.1
    
    Description: 
    
        Using Error handlers.
    
    Usage:
    
        python __init__.py -name <name> 
    
    Parameters:
    
        Parameter Properties   Aliases   Description                Required   
        -name     <name>                 Display the name passed.   Yes        

#### Code:
```python
import sys
from parameterparser import Cluster, Parameter, Parser

# Initialize the Cluster
parameters = Cluster()

# Create the Parameter
name_parameter = Parameter("-", "name", lambda name: name)

# Set the description for the parameter
name_parameter.set_description("Display the name passed.")

# Make the parameter required
name_parameter.set_required(True)

# Add the Parameter to the Cluster
parameters.add(name_parameter)

# Create the Parameter Parser using the default argv
parser = Parser(sys.argv, parameters)

# Set the error handler closure that will be called when an error
# is encountered while parsing a parameter that exists in the
# pre defined parameter cluster. This function will also be called when
# a required parameter is not supplied.
#
# This takes a Callable. Here we use a lambda.
parser.set_error_handler(lambda error: print(str(error)))

# Parse the arguments using the Cluster.
results = parser.parse()

# Check the validity of the parser, if it's not valid
# print the usage. Otherwise, output the results.
if not parser.is_valid() or "name" not in results:
    parameters.print_full_usage(
        "Parameter Parser",
        "Using Error handlers.",
        "v0.0.1"
    )
else:
    print("Your name is: " + results["name"])
```