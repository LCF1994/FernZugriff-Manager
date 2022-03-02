import subprocess


class ServidorSAGE:
    def __init__(self, ip, user='sagetr1', *args) -> None:
        self.ip = ip
        self.user = user
        self.reachable = None

    def __update_reachable(self) -> None:
        self.reachable = self.check_ping()

    def check_ping(self) -> bool:
        __ping = subprocess.run(
            ['ping', self.ip, '-w', '3'], stdout=subprocess.DEVNULL
        )
        return True if __ping.returncode == 0 else False

    def cmd(self, cmd: str) -> tuple:
        remote_cmd = subprocess.run(
            [
                'ssh',
                '-X',
                '-o',
                'ServerAliveInterval=5',
                self.user + '@' + self.ip,
                cmd,
            ],
            capture_output=True,
        )
        return remote_cmd.stdout, remote_cmd.stderr, remote_cmd.returncode

    def get_config(self):
        pass

    def set_config(self):
        pass

    def abre_visor_acesso(self):
        pass


if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.131')

    print(sage1.reachable)

    saida, err, err_code = sage1.cmd('var')
    saida_convertida = str(saida, 'utf-8')
    saida_splitlines = saida_convertida.splitlines()
    print('Saida do comando 1: ' + saida_convertida)

    saida, err, err_code = sage1.cmd('whoami')
    print('Saida do comando 2: ' + str(saida, 'utf-8'))
