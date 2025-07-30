from ussl.exceptions import SOARException


class ProtocolError(SOARException):
    """ Базовый класс, описывающий ошибки удаленного доступа. """
    pass


class ConnectionFailed(ProtocolError):
    """ Класс, описывающий ошибку подключения к удаленному хосту. """
    pass


class CredentialsError(ProtocolError):
    """ Класс, описывающий ошибку авторизации. """
    pass


class PermissionsError(ProtocolError):
    """ Класс, описывающий ошибку доступа. """
    pass


class ExecutionError(ProtocolError):
    """ Класс, описывающий ошибку выполнения команд. """
    pass
