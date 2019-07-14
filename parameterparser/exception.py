class ParseException(Exception):
    """
    Class used for representing Parse Exceptions.
    """
    # Error Codes
    INVALID_ARGUMENT_COUNT_ALIAS = 60001
    INVALID_ARGUMENT_COUNT_PARAMETER = 60002
    INVALID_ARGUMENT_COUNT_VARIADIC_ALIAS = 60003
    INVALID_ARGUMENT_COUNT_VARIADIC_PARAMETER = 60004
    MISSING_REQUIRED_ARGUMENT = 60005

    """
    :var parameter: The parameter that caused this Exception, if any.
    """
    parameter = None

    """
    :var message: The Message for this Exception.
    """
    message = None

    def __init__(self, message, code, parameter=None):
        """
        Initialize this Exception.
        :param message:   The message.
        :param code:      The Code.
        :param parameter: The Parameter if any.
        """
        super(ParseException, self).__init__(message)
        self.message = message
        self.code = code
        self.parameter = parameter

    def __str__(self):
        """
        Handle the conversion of this Exception into a String.
        :return: String value
        """
        return "ParseException: [" + str(self.code) + "] (parameter: " + (
            "UNKNOWN" if self.parameter is None else self.parameter.name
        ) + ") : " + self.message
