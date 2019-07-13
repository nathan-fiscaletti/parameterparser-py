## Index:
* [Example 1: Using Parameter Parser](./Example1.md)
* [Example 2: Using a Cluster](./Example2.md)
* [Example 3: Using a Cluster with Variadic Arguments (`*args`)](./Example3.md)
* [Example 4: Using Aliases](./Example4.md)
* [Example 5: Using Error Handlers](./Example5.md)
* [Example 6: Halting the Parser](./Example6.md)
* Example 7: Printing Usage

----
### Example 7 : Printing Usage

#### Usage: 
    python test.py
#### Output: 
    Parameter Parser v0.0.1
    
    Description: 
    
        Halting the Parser.
    
    Usage:
    
        myapp --read ( -rf ) <files, ...> [--load ( -rf ) <file>] 
    
    Parameters:
    
        Parameter Properties     Aliases   Description                  
        --load    <file>         -rf       Will load a file.            
        --read    <files, ...>   -rf       Will read a list of files.   
#### Code:
```python
from parameterparser import Cluster, Parameter

# Initialize the Cluster
parameters = Cluster()

# Create the Parameter
load_parameter = Parameter("--", "load", lambda file: file)\
                     .add_alias("lf", "-")\
                     .set_description("Will load a file.")
read_parameter = Parameter("--", "read", lambda *files: files)\
                     .set_required(True)\
                     .add_alias("rf", "-")\
                     .set_description("Will read a list of files.")

# Add the Parameter to the Cluster
parameters.add_many([load_parameter, read_parameter])

# Print the usage for the Cluster.
parameters.print_full_usage(

    # Required Parameters

    "Parameter Parser",     # Application Name
    "Halting the Parser.",  # Application Description

    # Optional Parameters

    "v0.0.1",               # Application Version
    "myapp",                # If not null, will replace the `python script.py` portion of the command line.
    True,                   # Show required parameters first in Usage. (Defaults to True)
    2,                      # The amount of padding to add to each column after the longest word. (Default 2)

    ["required"]            # You can specify which columns you would like hidden from the output here.
                            # This example hides the "required" output. See usage_style.py for a list of
                            # available column keys.

)
```
