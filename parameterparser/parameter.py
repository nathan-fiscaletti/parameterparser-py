import inspect
import sys


class Parameter:
    """
    Represents a Parameter.

    Attributes:
        :var name: The name of this Parameter.
        :var prefix: The prefix for this Parameter.
        :var closure: The lambda to execute for this Parameter.
        :var aliases: The aliases for this Parameter.
        :var parent: The parent Parameter for this Parameter, if any.
        :var description: The Description for this Parameter.
        :var required: Whether or not this Parameter is required, default False.
    """
    name = None
    prefix = None
    closure = None
    aliases = dict()
    parent = None
    description = None
    required = False

    def __init__(self, prefix, name, closure):
        """
        Create a new Parameter.
        :param prefix:  The prefix.
        :param name:    The name.
        :param closure: The closure.
        """
        self.prefix = prefix
        self.name = name
        self.closure = closure

    def has_parent(self):
        """
        Check if this Parameter has a Parent.
        :return: True if this Parameter has a parent.
        """
        return self.parent is not None

    def set_required(self, required):
        """
        Set this Parameter as Required.
        :param required: The value.
        :return: This Parameter following the Fluent design pattern..
        """
        self.required = required
        return self

    def set_description(self, description):
        """
        Set the Description for this Parameter.
        :param description: The Description.
        :return: This Parameter following the Fluent design pattern..
        """
        self.description = description
        return self

    def add_alias(self, name, prefix=None):
        """
        Add an Alias for this Parameter.
        :param name: The alias.
        :param prefix: The prefix for the alias, defaults to
                       this Parameters prefix.
        :return: This Parameter following the Fluent design pattern..
        """
        if prefix is None:
            self.aliases[self.prefix] = name
        else:
            self.aliases[prefix] = name
        return self

    def get_usage(self, encapsulate=True, with_aliases=True):
        """
        Retrieve the Usage for this Parameter as a String.
        :param encapsulate: Whether or not to encapsulate the usage, defaults to True.
        :param with_aliases: Whether or not to include aliases, defaults to True.
        :return: The usage for this Parameter.
        """
        usage = ""
        if encapsulate:
            usage = "" if self.required else "["
        aliases = self.get_alias_usage(encapsulate) if with_aliases else ""
        usage += self.prefix + self.name + aliases + " "
        usage += self.get_properties_usage()
        return usage + ("" if self.required else "]") if encapsulate else ""

    def get_alias_usage(self, encapsulate=True):
        """
        Retrieve the Alias usage as a String.
        :param encapsulate: Whether or not to encapsulate the usage, defaults to True.
        :return: The Alias usage as a String.
        """
        result = ""
        for prefix, alias in self.aliases.items():
            if encapsulate:
                result = " (" if result == "" else result + ","
                result = result + " " + prefix + alias
            else:
                result = prefix + alias if result == "" else result + ", " + prefix + alias
        if encapsulate:
            result = result + ("" if result == "" else " )")
        return result

    def get_arg_spec(self):
        # noinspection SpellCheckingInspection
        """
        Retrieve the arg spec for this Parameters closure argument.
        :return: The argspec (2.7+) or fullargspec (3.0+)
        """
        if sys.version_info[0] < 3:
            # noinspection PyDeprecation
            arg_spec = inspect.getargspec(self.closure)
        else:
            arg_spec = inspect.getfullargspec(self.closure)
        return arg_spec

    def get_properties_usage(self):
        """
        Retrieve the properties for this parameter as a string.
        :return: The properties for this parameter as a string.
        """
        result = ""
        arg_spec = self.get_arg_spec()
        for arg in list(arg_spec.args):
            result = result + ("" if result == "" else " ") + "<" + arg + ">"
        if arg_spec.varargs is not None:
            result += ("" if result == "" else " ") + "<"
            result += arg_spec.varargs + ", ...>"
        if arg_spec.varkw is not None:
            raise Exception("Parameter Parser does not support ** arguments.")

        return result
