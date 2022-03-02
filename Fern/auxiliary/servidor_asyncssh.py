import asyncio, asyncssh, sys

class ServidorSAGE:
    def __init__(self, host:str, username='sagetr1', password='sagetr1') -> None:
        self.host = host
        self.username = username
        self.password = password
   
    def create_connection(self) -> asyncssh.connection.SSHClientConnection:
        conn_options = asyncssh.SSHClientConnectionOptions(username=self.username, password=self.password, x11_forwarding='ignore_failure', known_hosts=None)
        return asyncssh.connect(self.host, options=conn_options)

    async def exec_cmd(self, cmd:str, *args, **kargs) -> tuple:
        async with self.create_connection() as conn:
            result = await conn.run(cmd, check=True)
            return result.stdout[:-1], result.returncode, result.exit_status




if __name__ == '__main__':
    sage1 = ServidorSAGE('192.168.198.134')

    try:
        r = asyncio.run(
            asyncio.to_thread(sage1.exec_cmd('whoami')))
        print(r)

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SSH connection failed: ' + str(exc))
