
class UsageStyle:
    @staticmethod
    def all(column_padding):
        return UsageStyle.all_except(dict(), column_padding)

    @staticmethod
    def all_except(ex, column_padding):
        result = {
            "parameter": {
                "longest": 9,
                "values": [],
                "fetch": lambda parameter: parameter.prefix+parameter.name
            },
            "properties": {
                "longest": 10 + column_padding,
                "values": [],
                "fetch": lambda parameter: parameter.get_properties_usage()
            },
            "aliases": {
                "longest": 7 + column_padding,
                "values": [],
                "fetch": lambda parameter: parameter.get_alias_usage(False)
            },
            "description": {
                "longest": 11 + column_padding,
                "values": [],
                "fetch": lambda parameter: "" if parameter.description is None else parameter.description
            },
            "required": {
                "longest": 8 + column_padding,
                "values": [],
                "fetch": lambda parameter: "Yes" if parameter.required else ""
            }
        }
        for e in ex:
            del result[e]
        return result
