import asyncio
import sys

import asyncssh
from kivy.logger import Logger


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
        self.target_ip = None

        self._terminal_default = 'xterm -sb -sl 3000 -T "Terminal" -geometry 160x17+0-0 -fg green -bg black'

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
            Logger.debug('Asyncssh : Task Cancelled')

    def run_thread(self, cmd: str, *args):
        try:
            return asyncio.run(self._wait_for_thread(cmd))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))

    def run_task(self, cmd: str, *args):
        try:
            return asyncio.run(self._wait_for_task(cmd))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))

    def open_visor_acesso(self) -> None:
        # _visor_acesso = 'xterm -sb -sl 3000 -n SysLog -T "Log do VisorAcesso" -geometry 160x17+0-0 -fg green -bg black -e VisorAcesso'
        _visor_acesso = 'VisorAcesso'
        self.run_task(_visor_acesso)

    def close_visor_acesso(self) -> None:
        self.task.cancel()

    def open_syslog(self) -> None:
        slog = 'xterm -sb -sl 3000 -n SysLog -T "Log de Mensagens do Sistema Operacional" -geometry 160x17+0-0 -fg black -bg cyan -e tail -f $LOG/unix.log'
        self.run_thread(slog)

    def open_remote_terminal(self) -> None:
        self.run_thread(self._terminal_default)

    def change_target_ip(self, new_ip: str) -> None:
        self.change_target_ip = new_ip

    def ping_target(self) -> None:
        _remote_ping = (
            f'{self._terminal_default} -e ping {self.target_ip} -w 3'
        )
        self.run_thread(_remote_ping)


if __name__ == '__main__':
    sage1 = AsyncSSHClient('192.168.198.11')
