# Parameter Parser: Clusters

See: [parameterparser/cluster.py](../parameterparser/cluster.py)

A Cluster is a group of Parameters packaged together.

## Creating a Parameter Cluster

See [Example 2 : Using a Cluster](../examples/Example2.md)

```python
from parameterparser import Cluster
cluster = Cluster()
```

## Adding a Parameter to a Cluster

To add a Parameter to a Cluster, first [create your parameter](./Parameters.md), and then use one of the following functions:

|Function|Effect|
|---|---|
|`add(Parameter)`|Adds a Parameter to the Cluster.|
|`addMany(array[Parameter])`|Adds multiple Parameters to the Cluster at once.|


You can also remove a Parameter from the cluster using one of the following functions:

|Function|Effect|
|---|---|
|`remove(string, string)`|Removes a Parameter from the cluster. The first argument is the Prefix for the Parameter and the second is the name of the Parameter.|

## Setting the Default Handler

See [Example 1: Using Parameter Parser](../examples/Example1.md)

If an argument is found during parsing that does not match any of the configured Parameters the Default Handler will be called. You can configure how this performs using the following:

```python
def default_handler(argument):
    # handle the argument
    return argument
    
parameters.set_default(default_handler)

# Alternately, you can use a lambda
parameters.set_default(lambda argument: argument)
```

> The Cluster object implements the [Fluent](https://en.wikipedia.org/wiki/Fluent_interface) design pattern, so you can chain these functions.

## Printing Usage

See: [Example 7: Printing Usage](../examples/Example7.md)

You can print the usage for your Cluster using the following:

```python
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