from ussl.exceptions import SOARException


class DataError(SOARException):
    """ Базовый класс для ошибок валидации. """
    pass


class NoInputError(DataError):
    """ Класс для ошибок отсутствия обязательных входных данных. """
    pass


class NoSecretsError(DataError):
    """ Класс для ошибок отсутствия обязательных секретов. """
    pass


class BadInputError(DataError):
    """ Класс для ошибок неверных входных данных. """
    pass


class BadSecretsError(DataError):
    """ Класс для ошибок неверных секретов. """
    pass
