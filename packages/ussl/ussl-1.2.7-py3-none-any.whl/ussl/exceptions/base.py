import json
from typing import List, Union


class SOARException(Exception):
    """
    Стандартный класс для исключений скриптов.

    Публичные поля и свойства:
        ``message``(Union[List[str], str, dict]): информация об исключении
        ``error_code``(str): название исключения
    """

    message: str = None

    @property
    def error_code(self):
        return self.__class__.__name__

    def __init__(self, message: Union[List[str], str, dict, Exception, None] = None):
        if message is None:
            self.message = ' '
        elif isinstance(message, Exception):
            self.message = str(message)
        elif isinstance(message, list):
            self.message = ', '.join(message)
        elif isinstance(message, dict):
            self.message = json.dumps(message)
        elif isinstance(message, str):
            self.message = message
        else:
            raise TypeError('Message must be str, list, dict or Exception')

    def __str__(self):
        return self.message
