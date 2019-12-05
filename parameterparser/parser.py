from parameterparser.cluster import Cluster
from parameterparser.parameter import Parameter
from parameterparser.result import Result
from parameterparser.exception import ParseException


class Parser:
    """
    Class used for parsing a string of parameters based on
    a Cluster provided and the parameters defined within.

    Attributes:
        :var valid: Whether or not this Parser is valid.
        :var error_handler: The error handler.
        :var halted_by: The parameter that halted this Parser, if any.
        :var results: The results that have been accumulated after a parse.
        :var invalid_param: The parameter that invalidated this parser, if any.
    """

    def __init__(self, argv=None, cluster=None):
        """
        Initialize the Parser.
        :param argv:    The string array to parse.
        :param cluster: The Cluster.
        """
        self.error_handler = None
        self.__argv = None
        self.cluster = Cluster()
        self.__initialize(argv, cluster)

    def parse(self, argv=None, cluster=None):
        """
        Parse the array of strings and retrieve the results.
        :param argv:    The array of strings.
        :param cluster: The Cluster
        :return:        The results.
        """
        self.__initialize(argv, cluster)
        self.__check_validity_and_continue_parse()
        return self.results

    def set_error_handler(self, handler):
        """
        Set the error handler.
        :param handler: The error handler.
        :return: This parser.
        """
        self.error_handler = handler
        return self

    def set_default(self, default):
        """
        Set the default handler.
        :param default: The handler.
        :return: This parser.
        """
        self.cluster.set_default(default)

    def is_valid(self):
        """
        Check if this parser is valid.
        :return: True if it's valid, False otherwise.
        """
        return self.valid

    def __initialize(self, argv, cluster):
        """
        Initialize the Parser.
        :param argv:    The string array to parse.
        :param cluster: The Cluster.
        """
        self.valid = True
        # noinspection PyTypeChecker
        self.halted_by = None
        self.__cursor = 0
        self.results = {}
        # noinspection PyTypeChecker
        self.invalid_param = None
        if cluster is not None:
            self.cluster = cluster
            if argv is not None:
                self.__preload_aliases()
        if argv is not None:
            self.__preload_parameters(argv[:])

    def __preload_aliases(self):
        """
        Load the Aliases for the cluster into their own
        Parameter Objects so that they can properly be parsed.
        """
        dict_copy = dict(self.cluster.prefixes)
        for prefix in dict_copy.keys():
            parameters = dict_copy[prefix]
            for parameter_key in parameters.keys():
                parameter = parameters[parameter_key]
                for alias_prefix in parameter.aliases.keys():
                    alias_name = parameter.aliases[alias_prefix]
                    alias_param = Parameter(
                        alias_prefix,
                        alias_name,
                        parameter.closure
                    )
                    alias_param.parent = parameter
                    self.cluster.add(alias_param)

    def __preload_parameters(self, argv):
        """
        Preload the string of parameters to be parsed by joining
        entries that exist between quotes into their own single entry.
        :param argv: The array of strings.
        """
        argv.pop(0)
        self.__argv = []
        if len(argv) > 0:
            parsed = argv.pop(0)
            while parsed is not None:
                potential_quote = parsed[:-(len(parsed) - 1)]
                if potential_quote == "'":
                    self.__parse_quote(argv, parsed, quote_type="'")
                elif potential_quote == "\"":
                    self.__parse_quote(argv, parsed, quote_type="\"")
                else:
                    self.__argv.append(parsed)
                parsed = argv.pop(0) if len(argv) > 0 else None

    def __parse_quote(self, argv, parameter_str, quote_type):
        """
        Parse all data between two matching quotes of type quote_type.
        :param argv:          The array of Strings.
        :param parameter_str: The initial string.
        :param quote_type:    The quote type (" or ')
        """
        if parameter_str[-1:] == quote_type:
            self.__argv.append(parameter_str[1:-1])
        else:
            self.__argv.append(parameter_str[1:])
            if len(argv) > 0:
                parsed_part = argv.pop(0)
                while parsed_part is not None \
                        and parsed_part[-1:] != quote_type:
                    self.__argv[len(self.__argv) - 1] += " " + parsed_part
                    parsed_part = argv.pop(0) if len(argv) > 0 else None
                if parsed_part is not None:
                    self.__argv[len(self.__argv) - 1] \
                        += " " + parsed_part[0:-1]

    def __check_validity_and_continue_parse(self):
        """
        Verify that all required parameters exist and continue parsing.
        """
        if not self.__validate_required():
            error = ParseException(
                "Missing required argument: " + self.invalid_param.name,
                ParseException.MISSING_REQUIRED_ARGUMENT,
                self.invalid_param
            )
            if self.error_handler is not None:
                self.error_handler(error)
            else:
                raise error
            self.valid = False
        else:
            self.__parse_every()

    def __validate_required(self):
        """
        Verify that all required parameters exist within the array of strings.
        :return: True if all required parameters exist, false otherwise.
        """
        result = True
        for prefix in self.cluster.prefixes.keys():
            parameters = self.cluster.prefixes[prefix]
            for parameter_key in parameters.keys():
                parameter = parameters[parameter_key]
                if parameter.required:
                    if parameter.prefix + parameter.name not in self.__argv:
                        alias_found = False
                        for alias_prefix, alias in parameter.aliases.items():
                            if alias_prefix + alias in self.__argv:
                                alias_found = True
                        if not alias_found:
                            self.invalid_param = parameter \
                                if self.invalid_param is None \
                                else self.invalid_param
                            result = False
        return result

    def __parse_every(self):
        """
        Parse each parameter from the array of strings.
        """
        while self.__cursor < len(self.__argv):
            parameter_str = self.__argv[self.__cursor]
            if not self.__parse_single(parameter_str):
                break

    def __parse_single(self, parameter_str):
        """
        Parse a Single parameter from the array of strings.
        :param parameter_str: The parameter string to parse.
        :return: False if a parameter was invalid or the parser was halted.
        """
        if self.__prefix_exists(parameter_str):
            parameter = self.__get_parameter(parameter_str)
            if parameter is not None:
                arg_spec = parameter.get_arg_spec()
                args = list(arg_spec.args)
                if len(args) > 0 or arg_spec.varargs is None:
                    self.__parse_uniadic(parameter, len(args))
                if arg_spec.varargs is not None:
                    self.__parse_variadic(parameter)
                if not self.is_valid():
                    return False
                result_key = self.__get_real_name(parameter_str)
                result = self.results[result_key]
                if not isinstance(result, Result):
                    if result == Result.HALT_PARSE:
                        self.halted_by = parameter
                        del self.results[result_key]
                        return False
                else:
                    if result.should_halt():
                        self.halted_by = parameter
                        if result.value == Result.HALT_PARSE:
                            del self.results[result_key]
                        else:
                            self.results[result_key] = result.value
                        return False
            else:
                self.__respond_default(parameter_str)
        else:
            self.__respond_default(parameter_str)
        return True

    def __parse_uniadic(self, parameter, count):
        """
        Parse a Uniadic parameter and increment the cursor.
        :param parameter: The parameter.
        :param count:     The number of arguments.
        """
        closure_arguments = []
        current_argument = 0
        while current_argument < count \
                and len(self.__argv) > (self.__cursor + 1):
            closure_arguments.append(self.__argv[self.__cursor + 1])
            current_argument += 1
            self.__increment_cursor()
        if len(closure_arguments) == count:
            name = parameter.name \
                if not parameter.has_parent() \
                else parameter.parent.name
            self.results[name] = parameter.closure(*closure_arguments)
        else:
            self.valid = False
            error = ParseException(
                "Invalid argument count. Expecting " +
                str(count) + " but received "
                + str(len(closure_arguments)) + ".",
                ParseException.INVALID_ARGUMENT_COUNT_ALIAS
                if parameter.has_parent()
                else ParseException.INVALID_ARGUMENT_COUNT_PARAMETER,
                parameter
            )
            if self.error_handler is not None:
                self.error_handler(error)
            else:
                raise error
        self.__increment_cursor()

    def __parse_variadic(self, parameter):
        """
        Parse a variadic parameter and increment the cursor.
        :param parameter: The parameter.
        """
        self.__increment_cursor()
        closure_arguments = []
        available = len(self.__argv) >= self.__cursor
        argument = None
        if available:
            argument = self.__argv[self.__cursor]
        while available and argument is not None \
                and not self.__prefix_exists(argument):
            closure_arguments.append(argument)
            self.__increment_cursor()
            available = len(self.__argv) > self.__cursor
            argument = None
            if available:
                argument = self.__argv[self.__cursor]
        if len(closure_arguments) > 0:
            name = parameter.name \
                if not parameter.has_parent() else parameter.parent.name
            self.results[name] = parameter.closure(*closure_arguments)
        else:
            self.valid = False
            error = ParseException(
                "Invalid argument count. Expecting 1+ but received " +
                str(len(closure_arguments)) + ".",
                ParseException.INVALID_ARGUMENT_COUNT_VARIADIC_ALIAS
                if parameter.has_parent()
                else ParseException.INVALID_ARGUMENT_COUNT_VARIADIC_PARAMETER,
                parameter
            )
            if self.error_handler is not None:
                self.error_handler(error)
            else:
                raise error

    def __respond_default(self, parameter_str):
        """
        Respond with the default handler.
        :param parameter_str: The parameter string.
        """
        param_result = self.cluster.default(parameter_str)
        if param_result == -1:
            self.valid = False
        self.results[parameter_str] = param_result
        self.__increment_cursor()

    def __increment_cursor(self):
        """
        Increment the cursor.
        """
        self.__cursor += 1

    def __get_closure(self, parameter_str):
        """
        Retrieve a closure for a Parameter matching a string parameter.
        :param parameter_str: The string parameter.
        :return: The closure.
        """
        parameter = self.__get_parameter(parameter_str)
        return parameter.closure

    def __get_real_name(self, parameter_str):
        """
        Get the real name for a parameter based on a string parameter. If the
        parameter found has a parent, the parent name will be returned.
        :param parameter_str: The string parameter.
        :return: The real name.
        """
        parameter = self.__get_parameter(parameter_str)
        return parameter.name \
            if not parameter.has_parent() else parameter.parent.name

    def __get_parameter(self, parameter_str):
        """
        Retrieve a Parameter based on a parameter string.
        :param parameter_str: The parameter string.
        :return: The parameter.
        """
        last_prefix = None
        parameter_parsed = None
        for prefix in self.cluster.prefixes.keys():
            if parameter_str[0:len(prefix)] == prefix:
                parameter_str_without_prefix = parameter_str[len(prefix):]
                if parameter_str_without_prefix \
                        in self.cluster.prefixes[prefix]:
                    if last_prefix is None or len(last_prefix) < len(prefix):
                        last_prefix = prefix
                        parameter_parsed = parameter_str_without_prefix
        if last_prefix is not None and parameter_parsed is not None:
            return self.cluster.prefixes[last_prefix][parameter_parsed]
        return None

    def __prefix_exists(self, parameter_str):
        """
        Check if the prefix for a string parameter exists in the cluster.
        :param parameter_str: The parameter string
        :return: True if it exists, false otherwise.
        """
        return self.__get_prefix(parameter_str) is not None

    def __get_prefix(self, parameter_str):
        """
        Retrieve a prefix for a parameter that exists in our cluster
        based on a string parameter.
        :param parameter_str: The string parameter.
        :return: The prefix, or None
        """
        last_prefix = None
        for prefix in self.cluster.prefixes.keys():
            if parameter_str[:len(prefix)] == prefix:
                if last_prefix is None:
                    last_prefix = prefix
                else:
                    if len(last_prefix) < len(prefix):
                        last_prefix = prefix
        return last_prefix
