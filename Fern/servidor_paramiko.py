from paramiko import (
    AuthenticationException,
    AutoAddPolicy,
    SSHClient,
    SSHException,
)


class ServidorSAGE:
    def __init__(
        self, server_ip_or_hostname, user='sagetr1', password='sagetr1'
    ) -> None:
        # Server config
        self.ip = server_ip_or_hostname
        self.user = user
        self.password = password

        # SSH Client from Paramiko
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        # Internal variables for status

    def connect(self) -> None:
        try:
            self.client.connect(
                self.ip, username=self.user, password=self.password
            )
            # transport = self.client.get_transport()
            print('Conectado')
            # transport.open_x11_channel((self.ip,6010))

        except AuthenticationException:
            print('Erro de autenticação')
        except SSHException:
            print('Falha de conexão')

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

    def get_config(self):
        pass

    def set_config(self):
        pass

    def abre_visor_acesso(self):
        pass


if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.131')
    sage1.connect()

    print(sage1.get_var())
    # print(sage1.check_gcd_running())
    sage1.client.close()
