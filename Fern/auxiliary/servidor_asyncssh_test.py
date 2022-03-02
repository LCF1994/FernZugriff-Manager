import asyncio, asyncssh, sys


def create_conn():
    options = asyncssh.SSHClientConnectionOptions(username='sagetr1', password='sagetr1', x11_forwarding='ignore_failure', keepalive_interval='1s', known_hosts=None)
    #conn_config = {'ServerAliveInterval': 5}
    return asyncssh.connect('192.168.198.132', options=options)
    

async def run_client() -> None:
    async with create_conn() as conn:
        result = await conn.run('whoami', check=True)
        # print( result.stdout, end='')
        return result.stdout


try:
    r = asyncio.run(run_client())
    print(r)

except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
