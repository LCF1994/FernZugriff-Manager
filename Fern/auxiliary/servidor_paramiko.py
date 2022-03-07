import socket
from ast import match_case
from cmath import e

from paramiko import (
    AuthenticationException,
    AutoAddPolicy,
    SSHClient,
    SSHException,
)


class ServidorSAGE:
    def __init__(
        self, host, username='sagetr1', password='sagetr1', port=22
    ) -> None:
        # Server config
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        # SSH Client from Paramiko
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        self.transport = None
        # Internal variables for status

        self.var = {
            'CPU': '',
            'SAGE_OS': '',
            'HOST': 'unknow',
            'SOM': 'unknow',
            'BASE': 'unknow',
            'MODELO': 'unknow',
            'VERSAO': 'xx-xx',
            'DIFUSAO': 'unknow',
            'GCD': 'unknow',
            'LOCAL': 'unknow',
        }

        self.status = {
            'cpu': 15,
            'memory': 6,
            'disk_sage': 85,
            'disk_arqs': 45,
            'disk_logs': 65,
        }

        self.gcd = False

    def set_host(self, value: str) -> None:
        self.host = value

    def check_connection(self) -> bool:
        try:
            transport = self.client.get_transport() if self.client else None
            return transport and transport.is_active()
        except AttributeError:
            return False

    def connect(self) -> bool:
        print(f'Connecting to {self.host}')
        try:
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
            )
            print('Conectado')

            self.transport = self.client.get_transport()
            self.transport.set_keepalive(30)
            return self.check_connection()

        except AuthenticationException:
            print('Erro de autenticação')
        except SSHException:
            print('Falha de conexão')
        except (socket.error, OSError) as err:
            print(f'Socket error: {err}')

        return False

    def exec_cmd(self, cmd: str, stdin=None) -> bytes:
        stdin, stdout, stderr = self.client.exec_command(cmd)
        if stderr.channel.recv_exit_status() != 0:
            return str(stderr.read()[:-1], 'utf-8')
        else:
            return str(stdout.read()[:-1], 'utf-8')

    def check_gcd_running(self) -> bool:
        return True if self.exec_cmd('pgrep gcd') else False

    def get_var(self) -> dict:
        self.var = {
            'CPU': self.exec_cmd('echo $CPU').lower(),
            'SAGE_OS': self.exec_cmd('echo $SAGE_SO'),
            'HOST': self.exec_cmd('echo $HOST'),
            'SOM': self.exec_cmd('echo $SERV_SOM')
            if 'Undefined' not in self.exec_cmd('echo $SERV_SOM')
            else 'Undefined',
            'BASE': self.exec_cmd('echo $BASE'),
            'MODELO': self.exec_cmd('echo $MODELO'),
            'VERSAO': self.exec_cmd(
                '/export/home/sagetr1/sage/bin/Linux_x86_64/GetVersaoSage'
            ),
            'DIFUSAO': self.exec_cmd('echo $METODO_DIFUSAO')
            if 'Undefined' not in self.exec_cmd('echo $METODO_DIFUSAO')
            else 'Undefined',
            'GCD': 'ativo' if self.check_gcd_running() else 'desativado',
            'LOCAL': self.exec_cmd('echo $LOCAL'),
        }
        return self.var

    def abre_visor_acesso(self):
        pass


if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.136')

    # sage1.check_gcd_running()

    print(sage1.connect())

    print(sage1.check_connection())

    from time import sleep

    sleep(60)

    print(sage1.check_connection())

    # print(sage1.get_var())
