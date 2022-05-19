import asyncio
import sys

from time import sleep

import asyncssh
from asyncssh import SSHClientConnection

import asynckivy as ak

class AsyncSSHClient:
    def __init__(
        self, host: str, username='sagetr1', password='sagetr1'
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.conn_options = asyncssh.SSHClientConnectionOptions(
            username=self.username,
            password=self.password,
            x11_forwarding='ignore_failure',
            known_hosts=None,
        )

        self.loop = None

    async def exec_cmd(self, cmd: str, *args, **kargs) -> tuple:
        async with asyncssh.connect(
            self.host, options=self.conn_options
        ) as conn:
            result = await conn.run(cmd, check=True)
            return result.stdout[:-1], result.returncode, result.exit_status

    async def _wait_for_thread(self, cmd: str, *args):
        loop = asyncio.get_event_loop()
        r = await loop.create_task(self.exec_cmd(cmd), name=cmd)
        return r

    async def _wait_for_task(self, cmd: str, *args):
        self.task = asyncio.create_task(self.exec_cmd(cmd), name='task')
        try:
            return await self.task
        except asyncio.CancelledError:
            print('CPF Cancelado')

    def run_thread(self, cmd: str, *args):
        try:
            # r = asyncio.run(self._wait_for_thread(cmd))
            r = asyncio.run(self._wait_for_task(cmd))
            return r

        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))

    def open_visor_acesso(self) -> None:
        _visor_acesso = 'xterm -sb -sl 3000 -n SysLog -T "Log do VisorAcesso" -geometry 160x17+0-0 -fg green -bg black -e VisorAcesso'
        self.run_thread(_visor_acesso)


    def open_syslog(self) -> None:
        # slog = 'xterm -sb -sl 3000 -n SysLog -T "Log de Mensagens do Sistema Operacional" -geometry 160x17+0-0 -fg black -bg cyan -e tail -f $LOG/unix.log'
        # self.run_thread(slog)
        print('cancela tudo')
        self.task.cancel()




if __name__ == '__main__':
    sage1 = AsyncSSHClient('192.168.198.11')
