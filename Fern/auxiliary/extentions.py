import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger


class Extentions:
    def __init__(self) -> None:
        self.running_clocks = {}
        self.widgets = {
            'SRV1': {},
            'SRV2': {},
            'TC1': {},
            'TC2': {},
        }
        self.observers = {}

    async def async_cmd(
        self, async_action, future_reaction, *args, **kwgars
    ) -> None:
        future_reaction(
            await ak.run_in_thread(lambda: async_action(*args, **kwgars))
        )

    def connect_to_server(self, server: ServidorSAGE) -> None:
        Logger.info(f'App : Connecting to {server.host}')
        ak.start(self.async_cmd(server.connect, self.connection_result))

    def connection_result(self, data: bool) -> None:
        if data is True:
            Logger.info('App : Server connected successfully')
            # send screen widgets result
            try:
                self.observers['CONN_STATE'].update_connenction(data)

            except KeyError:
                print(f'KeyError {KeyError.with_traceback}')
            except AttributeError:
                print('Function not found')

        else:
            Logger.error('App : Connection Fail')

    def add_clock(name: str, action) -> None:
        ...

    def cancel_clock(clock: str) -> None:
        ...

    def open_config(path: str):
        ...
