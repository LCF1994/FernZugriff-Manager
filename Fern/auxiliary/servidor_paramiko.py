from ast import match_case
from cmath import e
from paramiko import (AuthenticationException, AutoAddPolicy, SSHClient,
                      SSHException)
import socket


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

        # Internal variables for status

    def connect(self) -> bool:
        print(f'Connecting to {self.host}')
        try:
            self.client.connect(
                self.host, username=self.username, password=self.password,port=self.port
            )
            # transport = self.client.get_transport()
            print('Conectado')
            # transport.open_x11_channel((self.ip,6010))
            return True

        except AuthenticationException:
            print('Erro de autenticação')
        except SSHException:
            print('Falha de conexão')
        except socket.error:
             print(f'Socket error: {socket.error}')
        
        return False


    def exec_cmd(self, cmd) -> bytes:
        stdin, stdout, stderr = self.client.exec_command(cmd)
        if stderr.channel.recv_exit_status() != 0:
            return str(stderr.read(), 'utf-8')
        else:
            return str(stdout.read()[:-1], 'utf-8')

    def check_gcd_running(self) -> bool:
        return True if self.exec_cmd('pgrep gcd') else False

    def get_var(self) -> dict:
        return {
            'CPU': self.exec_cmd('echo $CPU'),
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
        }

    def abre_visor_acesso(self):
        pass


if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.132')
    #sage1.set_config('host', '192.168.198.132')
    #sage1 = ServidorSAGE('1')
    print(sage1.connect())

    #print(sage1.get_var())
    # print(sage1.check_gcd_running())
    #sage1.client.close()


