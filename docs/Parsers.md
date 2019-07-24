# Parameter Parser: Parsers

See: [parameterparser/parser.py](../parameterparser/parser.py)

A Parser is an object that will parse the supplied argument array using the [Parameters](./Parameters.md) stored in a [Cluster](./Clusters.md). You can use any array of strings here, however it is most common to use the `sys.argv` property in Python.

## Creating a Parser

To create a Parser use the following

```python
import sys
from parameterparser import Parser
parser = Parser(sys.argv, parameters)
```

Where `sys.argv` is your array of strings to be parsed, and `parameters` is your instance of [`parameterparser.Cluster`](../parameterparser/cluster.py) (see [Clusters](./Clusters.md))

## Executing the Parser

See [Example 2: Using a Cluster](../examples/Example2.md)

Once you have created a Parser, you can parse the arguments using the following:

```python
results = parser.parse()
```

The results of the parser execution will be stored in the array `results` and the `.is_valid()` flag will be set.

## Validating the Parser

See [Example 2: Using a Cluster](../examples/Example2.md)

After you have parsed your arguments using `.parse()` you can check their validity using `.is_valid()` and choose how you want to handle invalid results.

```python
if not parser.is_valid():
    parameters.print_full_usage(
        "Parameter Parser",
        "An example of Validitation",
    )
else:
    print(results)
```

## Setting Error Handlers

See [Example 5 : Using Error Handlers](../examples/Example5.md)

You can set an error handler that will receive all instances of `parameterparser.ParseException` that would normally be thrown. If you do not set a error handler, then these exceptions will simply be raised as normal.

```python
parser.set_error_handler(lambda error: print(error))
```

The error codes are as follows:

|Code|Description
|---|---|
|`60001`|Invalid argument count while parsing a Uniadic Alias.|
|`60002`|Invalid argument count while parsing a Uniadic Parameter.|
|`60003`|Invalid argument count while parsing a Variadic Alias.|
|`60004`|Invalid argument count while parsing a Variadic Parameter.|
|`60005`|Missing a required parameter.|

## Halting the Parser

See [Example 6: Halting the Parser](../examples/Example6.md)

You can halt the parser when you encounter a specific Parameter. This will cause the parser to parse no further parameters and stop execution, do this by returning one of the following options from the Parameter's closure.

|Option|Effect|
|---|---|
|`Result.halt(value)`|Return the value for the Parameter and then halt the Parser.|
|`Result.halt()`|Return no value for the Parameter and then halt the Parser.|


```python
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
    
load_parameter = Parameter("-", "load", load_handler)
```

You can check if the Parser was halted using `parser.halted_by`.

```python
if parser.halted_by is not None:
    print("Halted by: " + parser.halted_by.name)
```
