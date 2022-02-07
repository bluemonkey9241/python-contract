import abc


class Parameter:
    value = None
    error_message = 'Not initialized'
    valid_values_description = ''

    def __init__(self, name, html_name, value, valid_values_description):
        self.name = name
        self.html_name = html_name
        self.value = value
        self.valid_values_description = valid_values_description

    @abc.abstractmethod
    def set_value_from_string(self, value: str):
        return
