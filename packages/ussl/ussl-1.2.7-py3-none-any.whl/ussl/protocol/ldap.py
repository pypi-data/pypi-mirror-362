from typing import Optional, Union

import ldap
from ldap.ldapobject import LDAPObject

from ..model import ProtocolData, Response, Query
from .base import BaseProtocol
from ..exceptions import CredentialsError, ConnectionFailed, ExecutionError


class LDAPProtocol(BaseProtocol):
    name = 'ldap'
    _connection: Union[LDAPObject, None] = None

    def __init__(self, protocol: Optional[ProtocolData] = None, **kwargs):
        super().__init__(protocol, **kwargs)
        self.base: Optional[str] = None
        self._connection: Optional[LDAPObject] = None

    def connect(self) -> None:
        protocol = self.protocol
        server = f'ldap://{protocol.host}'
        ldap_login = f'{protocol.username}@{protocol.domain}'
        self.base = ', '.join(f'dc={i}' for i in protocol.domain.split('.'))
        try:
            self._connection = ldap.initialize(server, bytes_mode=False)
            self._connection.protocol_version = ldap.VERSION3
            self._connection.timeout = self.CONNECT_TIMEOUT
            self._connection.set_option(ldap.OPT_REFERRALS, 0)
            self._connection.simple_bind_s(ldap_login, protocol.password)
        except ldap.INVALID_CREDENTIALS:
            raise CredentialsError()
        except ldap.SERVER_DOWN:
            raise ConnectionFailed("Ldap server is down")
        except Exception as e:
            raise ConnectionFailed(str(e))

    def close(self) -> None:
        try:
            self._connection.unbind()
        except Exception as e:
            raise ExecutionError("Unknown error while closing connection: " + str(e))
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def execute(self, query: Query, error_ignore: bool = False) -> Response:
        pass
