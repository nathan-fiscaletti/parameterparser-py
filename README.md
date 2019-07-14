# Parameter Parser (Python)

> **Parameter Parser** is a simple library used to parse intricate parameters from an array of strings.

> **Hint:** This package is available through `Python PIP`.
> `pip install parameterparser` 

#### Supports Python 2.7+

[![PyPI version](https://badge.fury.io/py/parameterparser.svg)](https://badge.fury.io/py/parameterparser)
![PyPI - Downloads](https://img.shields.io/pypi/dm/parameterparser.svg)
[![GitHub issues](https://img.shields.io/github/issues/nathan-fiscaletti/parameterparser-py.svg)](https://github.com/nathan-fiscaletti/parameterparser-py/issues)
[![GitHub stars](https://img.shields.io/github/stars/nathan-fiscaletti/parameterparser-py.svg)](https://github.com/nathan-fiscaletti/parameterparser-py/stargazers)
![PyPI - License](https://img.shields.io/pypi/l/parameterparser.svg)

[Documentation](./docs/) - [Advanced Code Examples](./examples/readme.md) - [Looking for the PHP version?](https://github.com/nathan-fiscaletti/parameterparser)

### Features
* Parse command line parameters.
* Assign aliases to parameters.
* Custom closures for each command line parameter.
* Variadic closure support for arguments taking more than one value.
* Customize the way the command line is parsed.

### Example Usage
```python
import sys
from parameterparser import Parameter, Cluster, Parser

# Initialize a new Cluster
parameters = Cluster()

# Add a Parameter to the Cluster
parameter = Parameter("-", "name", lambda name: name)

parameter.set_required(True)\
         .set_description("Your name.")

parameters.add(parameter)

# Create a new Parser using the Cluster
parser = Parser(sys.argv, parameters)

# Parse the parameters using the Parser.
results = parser.parse()

# Verify that the parameters were valid after parsing.
if not parser.is_valid():
    # Since it was not valid, output usage.
    parameters.print_full_usage(
        "Parameter Parser",
        "An advanced parameter parser for PHP",
        "v1.0.0"
    )
else:
    # Retrieve the name from the results
    name = results['name']

    # Output the name
    print("Your name is " . name . os.linesep)
```

### Output
```
~/ python test.py -name 'Nathan Fiscaletti'

   Your name is Nathan Fiscaletti
```