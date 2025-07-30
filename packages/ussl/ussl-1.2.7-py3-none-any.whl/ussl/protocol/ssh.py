import io
import re
import socket
import time
from typing import Optional, Union

import paramiko
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException
from ussl.exceptions import PermissionsError

from ..model import ProtocolData, Query, Response
from .base import BaseProtocol
from ..exceptions import ConnectionFailed, ExecutionError, CredentialsError


class SSHProtocol(BaseProtocol):
    name = 'ssh'
    """
    A class used to represent a ssh connection to remote host

    :param host: hostname or ip address of remote server
    :param login: user login for remote connection
    :param password: user password for remote connection
    :param port: ssh port. default 22 If not specified
    """

    _connection: Optional[paramiko.SSHClient] = None

    def __init__(self, protocol: Optional[ProtocolData] = None, **kwargs):
        super().__init__(protocol, **kwargs)

    def connect(self):
        """Open SSH connection to remote host.

        :raises: CreateSSHConnectionError: if failed authentication
            or connection or establishing an SSH session
        """
        protocol = self.protocol
        host = protocol.host
        login = protocol.username
        domain = protocol.domain
        if domain is not None:
            login = f'{login}@{domain}'
        password = protocol.password
        port = protocol.port or 22
        ssh_key = protocol.pem_file
        try:
            self._connection = paramiko.SSHClient()
            self._connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if password:
                self._connection.connect(
                    hostname=host, username=login,
                    password=password, port=port,
                    look_for_keys=False, allow_agent=False,
                    timeout=self.CONNECT_TIMEOUT
                )
            elif ssh_key:
                keyfile = io.StringIO(ssh_key)
                self._connection.connect(
                    host, port, login,
                    pkey=RSAKey.from_private_key(keyfile),
                    timeout=self.CONNECT_TIMEOUT,
                    look_for_keys=False,
                    allow_agent=False
                )
        except AuthenticationException as error:
            raise CredentialsError(str(error))
        except (SSHException, socket.timeout) as exc:
            raise ConnectionFailed(str(exc))
        except Exception as error:
            raise ConnectionFailed(f'SSH connection failed: {error}')

    def close(self):
        """Close SSH connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    # def __enter__(self):
    #     self.connect()
    #     return self
    #
    # def __exit__(self, exc_type: Exception, *args):
    #     self.close()  ## TODO: make context manager
    #     if exc_type is not None:
    #         return False
    #     return True

    def execute(self, query: Union[Query, str], error_ignore: bool = False) -> Response:
        if self._connection is None:
            self.connect()
        if isinstance(query, str):
            query = Query(command=query)

        if query.shell_type == 'su' and query.sudo:
            return self._execute_su(query, error_ignore)
        if query.shell_type == 'su_root' and query.sudo:
            return self._execute_su_root(query, error_ignore)
        return self._execute_sudo(query, error_ignore)




    def _execute_su(self, query: Union[Query, str], error_ignore: bool = False) -> Response:
        if isinstance(query, str):
            query = Query(command=query)
        start_string_numb = 5 if query.sudo else 3
        command = query.command
        sudo = query.sudo
        timeout = query.timeout if query.timeout else self.EXECUTE_TIMEOUT
        command = f'su -c "{command}"\n'
        chan = self._connection.invoke_shell()
        chan.settimeout(timeout)
        chan.send(command.encode('utf-8'))
        time.sleep(2)
        if sudo:
            chan.send(f'{sudo}\n'.encode('utf-8'))
            time.sleep(2)
        output = chan.recv(-1).decode('utf-8')
        output = " ".join(output.split('\n')[start_string_numb:-1]).replace('\r', '')
        if "su: Сбой при проверке подлинности" in output:
            if self.EXECUTE_ERROR_IGNORE or error_ignore:
                return Response(result='PermissionsError',
                                status_code=1,
                                stderr=f'Invalid su password: {output}',
                                stdout=output)
            raise PermissionsError(f'Invalid su password: {output}')
        return Response(result='Command executed successfully',
                        status_code=0,
                        stderr="",
                        stdout=output)

    def _execute_su_root(self, query: Union[Query, str], error_ignore: bool = False) -> Response:
        if isinstance(query, str):
            query = Query(command=query)
        start_string_numb = 5 if query.sudo else 3
        sudo = query.sudo
        timeout = query.timeout if query.timeout else self.EXECUTE_TIMEOUT
        command = f'su -\n'
        chan = self._connection.invoke_shell()
        chan.settimeout(timeout)
        chan.send(command.encode('utf-8'))
        time.sleep(2)
        if sudo:
            chan.send(f'{sudo}\n'.encode('utf-8'))
            time.sleep(2)
        output = chan.recv(-1).decode('utf-8')
        output = " ".join(output.split('\n')[start_string_numb:-1]).replace('\r', '')
        if "su: Сбой при проверке подлинности" in output:
            if self.EXECUTE_ERROR_IGNORE or error_ignore:
                return Response(result='PermissionsError',
                                status_code=1,
                                stderr=f'Invalid su password: {output}',
                                stdout=output)
            raise PermissionsError(f'Invalid su password: {output}')
        command = f'{query.command}\n'
        chan.settimeout(timeout)
        chan.send(command.encode('utf-8'))
        output = chan.recv(-1).decode('utf-8')
        output = " ".join(output.split('\n')[start_string_numb:-1]).replace('\r', '')
        chan.close()
        return Response(result='Command executed successfully',
                        status_code=0,
                        stderr="",
                        stdout=output)


    def _execute_sudo(self, query: Union[Query, str], error_ignore: bool = False) -> Response:
        if isinstance(query, str):
            query = Query(command=query)
        command = query.command
        sudo = query.sudo
        timeout = query.timeout if query.timeout else self.EXECUTE_TIMEOUT
        if sudo:
            command = f'sudo -S {command}'
        stdin, stdout, stderr = self._connection.exec_command(
            command=command,
            timeout=timeout)
        if sudo:
            stdin.write(sudo + "\n")
            stdin.flush()
            time.sleep(1)

        output = stdout.read().decode('utf-8').strip()
        if not query.raw_output:
            output = [line.strip() for line in output.split('\n') if line.strip()]

        error = stderr.read().decode('utf-8')
        if query.sudo:
            error = re.sub(rf"\[sudo] пароль для \w+:", "", error)
            error = re.sub(rf"\[sudo] password for \w+:", "", error)
        
        error = error.strip()
        if not query.raw_output:
            error = [line.strip() for line in error.split('\n') if line.strip()]

        if not output and error:
            if self.EXECUTE_ERROR_IGNORE or error_ignore:
                return Response(result=f'Command "{command}" executed failed',
                                status_code=1,
                                stderr=error,
                                stdout=output)
            raise ExecutionError(str(error) + str(output) + f'\nCommand: {command}')
        else:
            return Response(result='Command executed successfully',
                            status_code=0,
                            stdout=output,
                            stderr=error)
