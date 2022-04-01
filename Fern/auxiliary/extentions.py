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
                Logger.debug(
                    f'Clock : Conn_Checker - {server.name} [IP: {server.host}] - Connection Verified'
                )
                self._clock_gcd_checker(server)
            else:
                self.conn_status = True
                Logger.info(
                    f'App : {server.name} [IP: {server.host}] connected successfully'
                )

                # send screen widgets result
                try:
                    for widget in self.widgets[server.name].values():
                        try:
                            widget.update_connection(data)
                        except AttributeError:
                            Logger.debug(
                                'App : Function not found or not implemented'
                            )
                        continue

                except KeyError:
                    Logger.debug(
                        f'KeyError : {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
                    )

                # Check GCD
                self._clock_gcd_checker(server)

                # add Clock
                Logger.info('Clock : Conn_Checker added.')
                self.add_clock(
                    'Conn_Checker',
                    partial(self._clock_conn_checker, server),
                    5,
                )

        else:
            Logger.error('App : Connection Fail')
            if self.conn_status:
                self.clear_clocks()
                Logger.info('Clock : All clocks canceled')

    def gcd_result(self, data: bool, server: ServidorSAGE) -> None:
        # send screen widgets result
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_gcd_state(data)
                except AttributeError:
                    continue

        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

        if data is True:
            Logger.debug(
                f'Clock : GCD_Checker - {server.name} [IP: {server.host}] - GCD Running'
            )
            self._clock_charts_update(server)
        else:
            Logger.info(
                f'Clock : GCD_Checker - {server.name} [IP: {server.host}] - GCD Stopped'
            )

    def update_charts_with_data_received(
        self, data: dict, server: ServidorSAGE
    ) -> None:
        Logger.debug('Charts: Updating charts values')

        # send screen widgets result
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_charts_info(data)
                except AttributeError:
                    continue

        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def _on_open_process_card(self, server: ServidorSAGE) -> None:
        Logger.info('ProcessCard : Process_checker clock scheduled')
        self.add_clock(
            'Process_checker',
            partial(self._clock_update_proccess_list, server),
            10,
        )

    def _on_close_process_card(self) -> None:
        Logger.info('ProcessCard : Process_checker clock canceled')
        self.cancel_clock('Process_checker')

    def update_process_card(self, data: list, server: ServidorSAGE) -> None:
        Logger.info(
            f'ProcessCard : Data retrieved from {server.name} [IP: {server.host}]'
        )
        # send screen widgets result
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget._update_process(data)
                except AttributeError:
                    continue

        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def _clock_conn_checker(self, server: ServidorSAGE, *args) -> None:
        Logger.debug('Clock : Checking Connection State ...')
        ak.start(
            self.async_cmd_with_args(
                server.check_connection, self.connection_result, server
            )
        )

    def _clock_gcd_checker(self, server: ServidorSAGE, *args) -> None:
        Logger.debug(f'Clock : Checking {server.name} GCD State ...')
        ak.start(
            self.async_cmd_with_args(
                server.check_gcd_running, self.gcd_result, server
            )
        )

    def _clock_charts_update(self, server: ServidorSAGE, *args) -> None:
        Logger.debug(
            f'Clock : Requesting {server.name} Charts information ...'
        )
        ak.start(
            self.async_cmd_with_args(
                server.get_performance,
                self.update_charts_with_data_received,
                server,
            )
        )

    def _clock_update_proccess_list(self, server: ServidorSAGE, *args) -> None:
        Logger.info('Clock : Requesting Process Card data...')
        ak.start(
            self.async_cmd_with_args(
                server.get_server_proccess, self.update_process_card, server
            )
        )

    def add_clock(self, name: str, action, time_multplier: int) -> None:
        self.running_clocks[name] = Clock.schedule_interval(
            action, time_multplier * DEFAULT_TIME
        )

    def cancel_clock(self, clock: str) -> None:
        try:
            self.running_clocks[clock].cancel()
            Logger.debug('Clock : Clock successfully canceled')
        except KeyError:
            Logger.error('Clock : Clock not found.')

    def clear_clocks(self) -> None:
        for clock in self.running_clocks.values:
            clock.cancel()

    def open_config(path: str):
        ...
