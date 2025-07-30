from abc import ABC, abstractmethod
from typing import Optional

from ..model import Response, Query, ProtocolData


class BaseProtocol(ABC):
    EXECUTE_ERROR_IGNORE: bool = False
    EXECUTE_TIMEOUT: int = 2
    CONNECT_TIMEOUT: int = 5

    def __init__(self, protocol: Optional[ProtocolData] = None,
                 execute_error_ignore: Optional[bool] = None,
                 execute_timeout: Optional[int] = None,
                 connect_timeout: Optional[int] = None):
        self.protocol = protocol
        if execute_error_ignore is not None:
            self.EXECUTE_ERROR_IGNORE = execute_error_ignore
        if execute_timeout is not None and execute_timeout > 0:
            self.EXECUTE_TIMEOUT = execute_timeout
        if connect_timeout is not None and connect_timeout > 0:
            self.CONNECT_TIMEOUT = connect_timeout

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError('Метод connect не реализован')

    @abstractmethod
    def execute(self, query: Query, error_ignore: bool = False) -> Response:
        raise NotImplementedError('Метод execute не реализован')

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError('Метод close не реализован')
