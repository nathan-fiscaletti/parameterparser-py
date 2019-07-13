# Parameter Parser: Parameters

See: [parameterparser/parameter.py](../parameterparser/parameter.py)

## Creating a Parameter

See [Example 2 : Using a Cluster](../examples/Example2.md)

Creating a Parameter is very simple. Use the following code to create a new Parameter.

```python
from parameterparser import Parameter
parameter = Parameter("-", "name", lambda name: name)
```

This function takes the following arguments:

|Argument|Type|Description|
|---|---|---|
|`prefix`|`str`|The prefix for the Parameter.|
|`name`|`str`|The name for the Parameter.|
|`closure`|`Callable`|The closure used to process the Parameter.

## Configuring the Parameter

Once you have created a Parameter you can configure it using the following options:

|Function|Effect|
|---|---|
|`set_required(bool)`|Makes the Parameter a Required Parameter.|
|`set_description(str)`|Sets the description for the Parameter. This is used when displaying Parameter usage from a [Cluster](./Clusters.md))|
|`add_alias(str, str)`|Adds an Alias for this Parameter. The first parameter should be the Prefix for the Alias, and the second parameter should be the name of the Alias. _Note: Only one alias can exist per prefix per Parameter._ |

> The Parameter object implements the [Fluent](https://en.wikipedia.org/wiki/Fluent_interface) design pattern, so you can chain these functions.