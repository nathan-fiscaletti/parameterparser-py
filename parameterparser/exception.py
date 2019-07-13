class ParseException(Exception):
    INVALID_ARGUMENT_COUNT_ALIAS = 60001
    INVALID_ARGUMENT_COUNT_PARAMETER = 60002
    INVALID_ARGUMENT_COUNT_VARIADIC_ALIAS = 60003
    INVALID_ARGUMENT_COUNT_VARIADIC_PARAMETER = 60004
    MISSING_REQUIRED_ARGUMENT = 60005

    parameter = None
    message = None

    def __init__(self, message, code, parameter=None):
        super(ParseException, self).__init__(message)
        self.message = message
        self.code = code
        self.parameter = parameter

    def __str__(self):
        return "ParseException: [" + str(self.code) + "] (parameter: " + (
            "UNKNOWN" if self.parameter is None else self.parameter.name
        ) + ") : " + self.message
