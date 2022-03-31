from functools import partial

import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.logger import Logger

DEFAULT_TIME = 1


class Extentions:
    def __init__(self) -> None:
        self.running_clocks = {}
        self.widgets = {
            'SAGE_1': {},
            'SAGE_2': {},
            'THIN_1': {},
            'THIN_2': {},
        }
        self.conn_status = False

    async def async_cmd(self, async_action, future_reaction) -> None:
        future_reaction(await ak.run_in_thread(async_action))

    async def async_cmd_with_args(
        self, async_action, future_reaction, *args
    ) -> None:
        future_reaction(await ak.run_in_thread(async_action), *args)

    def connect_to_server(self, server: ServidorSAGE) -> None:
        Logger.info(f'App : Connecting to {server.name} [IP :{server.host}]')
        ak.start(
            self.async_cmd_with_args(
                server.connect, self.connection_result, server
            )
        )

    def connection_result(self, data: bool, server: ServidorSAGE) -> None:
        if data is True:
            if self.conn_status:
                Logger.info(
                    f'Clock : Conn_Checker - {server.name} [IP: {server.host}] - Connection Verified'
                )
            else:
                self.conn_status = True
                Logger.info(
                    f'App : {server.name} [IP: {server.host}] connected successfully'
                )

                # send screen widgets result
                try:
                    for widget in self.widgets[server.name].values():
                        widget.update_connenction(data)

                except KeyError:
                    print(
                        f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
                    )
                except AttributeError:
                    print('Function not found')

                # add Clock
                Logger.info('Clock : Conn_Checker added.')
                self.running_clocks['Conn_Checker'] = self.add_clock(
                    partial(self._clock_conn_checker, server), 5
                )

        else:
            Logger.error('App : Connection Fail')
            if self.conn_status:
                self.clear_clocks()
                Logger.info('Clock : All clocks canceled')

    def _clock_conn_checker(self, server, *args) -> None:
        Logger.info('Clock : Checking Connection State ...')
        ak.start(
            self.async_cmd_with_args(
                server.check_connection, self.connection_result, server
            )
        )

    # def _clock_conn_checker_result(self, *args):
    #    print(args)

    def add_clock(name: str, action, time_multplier: int) -> None:
        return Clock.schedule_interval(action, time_multplier * DEFAULT_TIME)

    def cancel_clock(self, clock: str) -> None:
        ...

    def clear_clocks(self) -> None:
        for clock in self.running_clocks.values:
            clock.cancel()

    def open_config(path: str):
        ...
