from parameter import Parameter


class NumericListParameter(Parameter):

    def __init__(self, name, html_name, value):
        Parameter.__init__(self, name, html_name, value,
                           'comma separated list of numbers')
        self.length = len(value)

    def set_value_from_string(self, value: str):  # FIXME validations
        self.error_message = ''
        self.value = list(map(lambda x: int(x),
                              value.replace(' ', '').split(',')))
