from parameter import Parameter


# FIXME: que los objetos tengan sentido (e.g. rangos coherentes).
class NumericParameter(Parameter):

    def __init__(self, name, html_name, value, lower_bound, upper_bound,
                 include_lower_bound, include_upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.include_lower_bound = include_lower_bound
        self.include_upper_bound = include_upper_bound
        Parameter.__init__(self, name, html_name,
                           self.set_value_from_string(value),
                           'must be greater{} than {} and less{} than {}'
                           .format(' or equal' if self.include_lower_bound else '', self.lower_bound,
                                   ' or equal' if self.include_upper_bound else '', self.upper_bound))

    def set_value_from_string(self, value: str):
        if value:
            # FIXME: conversion function should be an argument or rename NumericParameter to float parameter
            value = float(value)
            self.value = value
            if NumericParameter.check_number_is_in_range(value, self.lower_bound, self.upper_bound,
                                                         self.include_lower_bound, self.include_upper_bound):
                self.error_message = ''
                return value  # FIXME raro, es un set...
        self.error_message = '"{}" {}, but is {}.'.format(
            self.html_name,
            self.valid_values_description,
            self.value
        )

    # FIXME: merge as functional?
    @staticmethod
    def check_number_is_greater_than(number, value, include_value):
        if include_value:
            return number >= value
        else:
            return number > value

    @staticmethod
    def check_number_is_less_than(number, value, include_value):
        if include_value:
            return number <= value
        else:
            return number < value

    @staticmethod
    def check_number_is_in_range(number, lower_bound, upper_bound, include_lower_bound, include_upper_bound):
        return NumericParameter.check_number_is_greater_than(number, lower_bound, include_lower_bound) \
           and NumericParameter.check_number_is_less_than(number, upper_bound, include_upper_bound)
