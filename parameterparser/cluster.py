import sys
import os
from parameterparser.usage_style import UsageStyle


class Cluster:
    prefixes = {}
    default = None

    def __init__(self):
        self.default = lambda param: -1

    def add(self, parameter):
        if parameter.prefix not in self.prefixes.keys():
            self.prefixes[parameter.prefix] = dict()
        self.prefixes[parameter.prefix][parameter.name] = parameter
        return self

    def remove(self, prefix, name):
        del self.prefixes[prefix][name]
        return self

    def add_many(self, parameters):
        for parameter in parameters:
            self.add(parameter)
        return self

    def set_default(self, default):
        self.default = default

    def get_usage(self, required_first=False, custom_binary=None):
        if custom_binary is None:
            full_usage = "python " + os.path.basename(sys.argv[0]) + " "
        else:
            full_usage = custom_binary + " "
        for prefix in self.prefixes.keys():
            parameters = self.prefixes[prefix]
            keys = list(parameters.keys())
            if required_first:
                keys = sorted(parameters.keys(), key=lambda x: parameters[x].required, reverse=True)
            for parameter_name in keys:
                parameter = parameters[parameter_name]
                if not parameter.has_parent():
                    full_usage += parameter.get_usage() + " "

        return full_usage

    def print_full_usage(self, app_name, description, app_version=None,
                         custom_binary=None, required_first=True,
                         column_padding=2, excluding=None):
        if excluding is None:
            excluding = {}
        sys.stdout.write(os.linesep+app_name)
        sys.stdout.write(("" if app_version is None else " " + app_version) + os.linesep)
        sys.stdout.write(os.linesep)
        if description is not None:
            sys.stdout.write("Description: "+os.linesep+os.linesep)
            sys.stdout.write("\t"+description+os.linesep+os.linesep)
        sys.stdout.write("Usage:"+os.linesep+os.linesep+"\t")
        sys.stdout.write(self.get_usage(required_first, custom_binary))
        sys.stdout.write(os.linesep+os.linesep)
        usage_styles = UsageStyle.all_except(excluding, column_padding)
        parameter_count = 0
        for prefix in self.prefixes.keys():
            parameters = self.prefixes[prefix]
            for parameter_name in parameters.keys():
                parameter = parameters[parameter_name]
                if not parameter.has_parent():
                    parameter_count += 1
                    for style_name in usage_styles.keys():
                        style = usage_styles[style_name]
                        n_val = style["fetch"](parameter)
                        n_val_size = len(n_val)
                        if n_val_size + column_padding > style["longest"]:
                            usage_styles[style_name]["longest"] = n_val_size + column_padding
                        usage_styles[style_name]["values"].append(n_val)
        sys.stdout.write("Parameters:"+os.linesep+os.linesep)
        header_format = "\t"
        column_names = []
        parameter_format = ""
        parameter_values = []
        for style_name in usage_styles.keys():
            style = usage_styles[style_name]
            header_format += "%-"+str(style["longest"])+"s "
            column_names.append(style_name.title())
        for i in range(0, parameter_count):
            new_format = "\t"
            for style_name in usage_styles.keys():
                style = usage_styles[style_name]
                new_format += "%-"+str(style["longest"])+"s "
                parameter_values.append(style["values"][i])
            new_format += os.linesep
            parameter_format += new_format

        sys.stdout.write((header_format+os.linesep) % tuple(column_names))
        sys.stdout.write((parameter_format+os.linesep) % tuple(parameter_values))
