from typing import Union, Optional, Tuple

import winrm.exceptions
from requests.exceptions import ReadTimeout, ConnectTimeout, ConnectionError as RequestsConnectionError
from ussl.exceptions import SOARException
from winrm import Session
from winrm.exceptions import (
    AuthenticationError,
    WinRMError,
    WinRMOperationTimeoutError,
    WinRMTransportError,
)

from .base import BaseProtocol
from ..model import Response, ProtocolData, Query
from ..exceptions import ConnectionFailed, ExecutionError, CredentialsError, PermissionsError


class WinRMProtocol(BaseProtocol):
    """
    Протокол WinRM.
    Реализовано подключение к удаленному хосту на HTTP и HTTPS протоколах.
    Порты соответственно 5985 и 5986.
    Поддерживаются форматы NTLM и PLAINTEXT.
    """
    name = 'winrm'
    WINRM_PORT = 5985
    WINRM_SSL_PORT = 5986
    VALID_TRANSPORT = {'plaintext', 'ntlm'}
    _connection: Union[Session, None]

    def __init__(self, protocol: Optional[ProtocolData] = None, **kwargs) -> None:
        super().__init__(protocol, **kwargs)
        self._connection: Union[Session, None] = None

    def connect(self) -> None:
        protocol = self.protocol
        host = protocol.host
        username = protocol.username
        domain = protocol.domain
        password = protocol.password
        scheme = protocol.default('scheme', None)
        path = protocol.default('path', 'wsman')
        # Отправка запроса в кодировке 437 даёт ответ на анлийском языке
        # однако при преобразовании байтов в строку и использованием той же
        # кодировки русские символы отображаются некорректно. Для того чтобы
        # обойти эту проблему, для декодирования используется кодировка 866
        # encoding = protocol.default('encoding', 437)
        self._decoding = protocol.default('decoding', 866)
        window_width = protocol.default('window_width', 300)
        transport = protocol.default('transport', 'ntlm')

        if transport not in self.VALID_TRANSPORT:
            raise ConnectionFailed(f'{transport} protocol is not supported')

        # для BasicAuth явно преобразуем 'username' и 'password' из utf8 в cp1251, т.к. requests.auth.HTTPBasicAuth
        # по умолчанию преобразует utf8 строки в latin1, при этом bytes оставляет 'как есть'.
        # https://github.com/requests/requests/pull/3673
        _username: Union[str, bytes] = f'{domain}\\{username}'
        _password: Union[str, bytes] = password
        if transport == 'plaintext':
            _username = f'{domain}\\{username}'.encode('cp1251')
            _password = password.encode('cp1251')
        else:
            _username = f'{domain}\\{username}'
            _password = password

        self._connection, status = self._try_connect(host, (_username, _password), transport, scheme, path)
        if not self._connection and status:
            raise ConnectionFailed(status)

        try:
            self.execute(Query(command=f'mode con:cols={window_width}', timeout=10))
        except Exception as e:
            raise ExecutionError(e)

    def _try_connect(self, host: str,
                     credentials: Tuple[str, str],
                     transport: str,
                     scheme: str = None,
                     path: str = 'wsman') -> Tuple[Optional[Session], str]:
        if scheme is not None:
            try:
                session = self._create_health_check_session(host,
                                                            credentials,
                                                            transport,
                                                            scheme,
                                                            path)
                return session, ""
            except (ConnectTimeout, ConnectionError, RequestsConnectionError):
                return None, 'Timeout'
            except WinRMError as e:
                return None, str(e)
        result = ""
        for scheme in ('http', 'https'):
            try:
                session = self._create_health_check_session(host,
                                                            credentials,
                                                            transport,
                                                            scheme,
                                                            path)
                return session, ""
            except (ConnectTimeout, ConnectionError, RequestsConnectionError):
                pass
            except winrm.exceptions.WinRMError as e:
                result += str(e)
        return None, result if result else 'Timeout'

    def _create_health_check_session(self,
                                     host: str,
                                     credentials: Tuple[str, str],
                                     transport: str,
                                     scheme: str,
                                     path: str = 'wsman') -> Session:
        port = self.WINRM_SSL_PORT if scheme == 'https' else self.WINRM_PORT
        session = Session(f'{scheme}://{host}:{port}/{path}',
                          auth=credentials,
                          server_cert_validation='ignore',
                          transport=transport,
                          read_timeout_sec=self.CONNECT_TIMEOUT,
                          operation_timeout_sec=self.EXECUTE_TIMEOUT)
        # Проверка соединения с удаленным хостом
        session.protocol.open_shell()
        return session

    def close(self) -> None:
        # Закрытие сессии не требуется. После выполнения запросов сессия сама вызывает session.protocol.close_shell()
        self._connection = None

    def execute(
            self,
            query: Union[Query, str],
            error_ignore: bool = False
    ) -> Response:
        if self._connection is None:
            self.connect()
        if isinstance(query, str):
            query = Query(command=query)
        try:
            resource = self._execute_command(query)
        except SOARException as e:
            if self.EXECUTE_ERROR_IGNORE or error_ignore:
                return Response(result=f'Command "{query.command}" executed failed',
                                stderr=str(e),
                                status_code=e.return_code)
            raise e
        return resource

    def _execute_command(self, query: Query) -> Response:
        try:
            if query.shell_type == 'ps':
                response = self._connection.run_ps(query.command)
            else:
                response = self._connection.run_cmd(query.command)
            std_out, std_err, status_code = response.std_out, response.std_err, response.status_code
            if status_code != 0 and status_code == 2147942405:
                raise PermissionsError(std_out.decode(encoding=str(self._decoding), errors='ignore'))
            if status_code != 0:
                std_err = std_err.decode(encoding=str(self._decoding), errors='ignore').strip()
                raise ExecutionError(std_err)

            std_out = std_out.decode(encoding=str(self._decoding)).strip()
            return Response(
                result=std_out,
                stdout=f'Command {query.command} executed successfully',
                status_code=0)

        except WinRMTransportError as exc:
            raise ConnectionFailed(exc)

        except AuthenticationError as exc:
            raise CredentialsError(exc)

        except (WinRMOperationTimeoutError, ReadTimeout):
            raise ConnectionFailed('Connection timeout')

        except WinRMError as exc:
            raise ExecutionError(exc)


