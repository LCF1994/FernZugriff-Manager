import json
import socket

from paramiko import (
    AuthenticationException,
    AutoAddPolicy,
    SSHClient,
    SSHException,
)


class ServidorSAGE(object):
    def __init__(
        self,
        name: str,
        host: str,
        username='sagetr1',
        password='sagetr1',
        port=22,
    ) -> None:

        # Server config
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        # SSH Client from Paramiko
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        # Internal variables for status
        self.transport = None
        self.conn = False

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
            'GCD_COR': [0, 0, 1, 1],
            'LOCAL': 'unknow',
        }

        self.performance = {
            'cpu': 0,
            'memory': 0,
            'disk_sage': 0,
            'disk_arqs': 0,
            'disk_logs': 0,
        }

        self.gcd = False

        self.proccess = {}

    def set_config(self, config: dict) -> None:
        try:
            self.host = config['host']
            self.username = config['username']
            self.password = config['password']
            self.port = config['port']
        except KeyError:
            print('Keys expected = [ host, username, password, port ]')

    def check_connection(self) -> bool:
        try:
            transport = self.client.get_transport() if self.client else None
            return transport and transport.is_active()
        except AttributeError:
            return False

    def connect(self) -> bool:
        # print(f'Connecting to {self.host}')
        try:
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
            )
            # print('Conectado')

            self.transport = self.client.get_transport()
            self.transport.set_keepalive(30)
            self.check_gcd_running()
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
        self.gcd = True if self.exec_cmd('pgrep gcd') else False
        return self.gcd

    def get_var(self) -> dict:
        self.var = {
            'CPU': self.exec_cmd('echo $CPU').lower(),
            'SAGE_OS': self.exec_cmd('echo $SAGE_SO'),
            'HOST': self.exec_cmd('echo $HOST'),
            'SOM': self.exec_cmd('echo $DEVICE_SOM')
            if 'Undefined' not in self.exec_cmd('echo $DEVICE_SOM')
            else 'Servidor',
            'BASE': self.exec_cmd('echo $BASE'),
            'MODELO': self.exec_cmd('echo $MODELO'),
            'VERSAO': self.exec_cmd(
                '/export/home/sagetr1/sage/bin/Linux_x86_64/GetVersaoSage'
            ),
            'DIFUSAO': self.exec_cmd('echo $METODO_DIFUSAO')
            if 'Undefined' not in self.exec_cmd('echo $METODO_DIFUSAO')
            else 'Undefined',
            'GCD': 'ativo' if self.check_gcd_running() else 'desativado',
            'GCD_COR': [0, 1, 0, 1]
            if self.check_gcd_running()
            else [1, 0, 0, 1],
            'LOCAL': self.exec_cmd('echo $LOCAL')
            if 'Undefined' not in self.exec_cmd('echo $LOCAL')
            else self.exec_cmd('echo $HOST'),
        }
        return self.var

    def brsql_request(self, query: str, gcd_required=False) -> dict:
        context = '' if gcd_required else '-c $BD'
        cmd = f'brsql -s {query} --json {context}'

        result = self._conversion_json_to_dict(self.exec_cmd(cmd))
        print(type(result))

        return result
        # return cmd

    def _conversion_json_to_dict(self, received_json: json) -> dict:
        json_loaded = json.loads(received_json)

        if type(json_loaded) == list and len(json_loaded) > 0:
            return json_loaded

    def get_performance(self) -> dict:
        query = f""" 'select cpu_usage, mem_usage, disk_use_sage, disk_use_arqs, disk_use_log from noh where id == "{self.var['LOCAL']}"' """

        print(query)
        data_dict = self.brsql_request(query, gcd_required=True)

        print(f'Tipo de dado recebido{type(data_dict)}')
        if type(data_dict) is list and len(data_dict) > 0:
            data_dict = data_dict[0]

        if type(data_dict) is dict:
            try:
                self.performance['cpu'] = data_dict['cpu_usage']
                self.performance['memory'] = data_dict['mem_usage']
                self.performance['disk_sage'] = data_dict['disk_use_sage']
                self.performance['disk_arqs'] = data_dict['disk_use_arqs']
                self.performance['disk_logs'] = data_dict['disk_use_log']
            except KeyError:
                print('Query has returned an error.')

        return self.performance

    def get_server_proccess(self, noh=1) -> list:
        query = f""" 'select id, estad from inp where a_noh == {noh}' """
        self.proccess = self.brsql_request(query, gcd_required=self.gcd)

        return self.proccess

    def abre_visor_acesso(self):
        ...


if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.137')

    print(f'Connection :{sage1.connect()}')
    # sage1.client.invoke_shell()

    # sage1.check_gcd_running()
    # print(f'GCD: {sage1.check_gcd_running()}')
    # print(f'Var: {sage1.get_var()}')
    # print(sage1.get_performance())
    # print(sage1.get_var())

    query = """ 'select * from noh' """
    result = sage1.brsql_request(query)
    print(f'Query 1 : {result}\n')

    print(f'Proccess: {sage1.get_server_proccess(noh=1)}')

    # print(f'Query 2 : {sage1.brsql_request(query, True)}')
