import asyncio
import sys

import asyncssh


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

    async def exec_cmd(self, cmd: str, *args, **kargs) -> tuple:
        async with asyncssh.connect(
            self.host, options=self.conn_options
        ) as conn:
            result = await conn.run(cmd, check=True)
            return result.stdout[:-1], result.returncode, result.exit_status

    async def _wait_for_thread(self):
        loop = asyncio.get_event_loop()
        r = await loop.create_task(self.exec_cmd('VisorAcesso'))
        return r

    def run_thread(self):
        try:
            r = asyncio.run(self._wait_for_thread())
            return r

        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))


if __name__ == '__main__':
    sage1 = AsyncSSHClient('192.168.198.137')

    print(sage1.run_thread())
    # try:
    #     r = asyncio.run(sage1._wait_for_thread())
    #     print(r)

    # except (OSError, asyncssh.Error) as exc:
    #     sys.exit('SSH connection failed: ' + str(exc))
