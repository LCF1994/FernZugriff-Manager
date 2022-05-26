import platform
from functools import partial

import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore

DEFAULT_TIME = 1
CONFIG_PATH = './Fern/config.json'


class Extentions:
    def __init__(self) -> None:
        self.running_clocks = {}
        self.widgets = {
            'SAGE_1': {},
            'SAGE_2': {},
            'THIN_1': {},
            'THIN_2': {},
        }
        self.storage = JsonStore(CONFIG_PATH)

        self.autoswitch_target = None
        self.autoswitch_current = None
        self.autoswitch_active = False

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
            if server.conn_status:
                Logger.debug(
                    f'Clock : Conn_Checker - {server.name} [IP: {server.host}] - Connection Verified'
                )
                self._clock_gcd_checker(server)
            else:
                server.conn_status = True
                Logger.info(
                    f'App : {server.name} [IP: {server.host}] connected successfully'
                )
                try:
                    for widget in self.widgets[server.name].values():
                        try:
                            widget.update_connection(data, server)
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
                    f'Conn_Checker_{server.name}',
                    partial(self._clock_conn_checker, server),
                    5,
                )
        else:
            Logger.error('App : Connection Fail')
            self.disconnect(server)

        self.autoswitch_update_connection(data, server)

    def gcd_result(self, data: bool, server: ServidorSAGE) -> None:
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_gcd_state(data, server)
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
            self._clock_server_hot_update(server)

        else:
            Logger.debug(
                f'Clock : GCD_Checker - {server.name} [IP: {server.host}] - GCD Stopped'
            )

        self.autoswitch_update_gcd_state(data, server)

    def update_server_hot_data_received(
        self, data: bool, server: ServidorSAGE
    ) -> None:
        Logger.debug('Dashboard : Updating Server HOT')
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_server_hot(data)
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def update_charts_with_data_received(
        self, data: dict, server: ServidorSAGE
    ) -> None:
        Logger.debug('Charts: Updating charts values')
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
        clock_name = f'Process_checker_{server.name}'

        Logger.info(f'ProcessCard : {clock_name} clock scheduled')
        self.add_clock(
            clock_name,
            partial(self._clock_update_process_list, server),
            10,
        )

    def _on_close_process_card(self, server: ServidorSAGE) -> None:
        clock_name = f'Process_checker_{server.name}'
        Logger.info(f'ProcessCard : Canceling clock {clock_name}...')
        self.cancel_clock(clock_name)

    def update_process_card(self, data: list, server: ServidorSAGE) -> None:
        Logger.debug(
            f'ProcessCard : Data retrieved from {server.name} [IP: {server.host}]'
        )
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
        Logger.debug(f'Clock : Checking {server.name} Connection State ... ')
        ak.start(
            self.async_cmd_with_args(
                server.validate_connection,
                self.connection_result,
                server
                # server.check_connection, self.connection_result, server
            )
        )

    def _clock_gcd_checker(self, server: ServidorSAGE, *args) -> None:
        Logger.debug(f'Clock : Checking {server.name} GCD State ...')
        ak.start(
            self.async_cmd_with_args(
                server.check_gcd_running, self.gcd_result, server
            )
        )

    def _clock_server_hot_update(self, server: ServidorSAGE, *args) -> None:
        Logger.debug(f'Clock : Checking hot/stand by at {server.name}...')
        ak.start(
            self.async_cmd_with_args(
                server.check_server_hot,
                self.update_server_hot_with_data_received,
                server,
            )
        )

    def update_server_hot_with_data_received(
        self, data: bool, server: ServidorSAGE
    ) -> None:
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_server_hot(data)
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
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

    def _clock_update_process_list(self, server: ServidorSAGE, *args) -> None:
        Logger.debug('Clock : Requesting Process Card data...')
        ak.start(
            self.async_cmd_with_args(
                server.get_server_process, self.update_process_card, server
            )
        )

    def add_clock(self, name: str, action, time_multplier: int) -> None:
        self.running_clocks[name] = Clock.schedule_interval(
            action, time_multplier * DEFAULT_TIME
        )

    def cancel_clock(self, clock: str) -> None:
        try:
            self.running_clocks[clock].cancel()
            Logger.info(f'Clock : Clock {clock} successfully canceled')
        except KeyError:
            Logger.error('Clock : Clock not found.')

    def clear_clocks(self) -> None:
        for clock in self.running_clocks.values():
            clock.cancel()

    def set_ip_on_server_title(self, server):
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_ip(server.host)
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def save_config(self, server: ServidorSAGE) -> None:
        if self.SAGE_1.host == self.SAGE_2.host:
            Logger.warning('App : Identical IPs configured for Servers')
        self.storage.put(
            server.name,
            host=server.host,
            username=server.username,
            password=server.password,
            port=server.port,
        )

    def autoswitch_save_config(self) -> None:
        self.storage.put(
            'app',
            autoswitch=self.autoswitch_active,
        )

    def disconnect(self, server: ServidorSAGE) -> None:
        server.conn_status = False
        server.disconnect()
        self._disconnection_rotine(server)
        Logger.warning(f'App : {server.name} disconnected')

    def _disconnection_rotine(self, server: ServidorSAGE) -> None:
        if server.conn_supervision and self.autoswitch_active:
            self.autoswitch_trigger()
        else:
            if server.visor_acesso:
                self.cancel_visor_acesso(server)
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.update_connection(False, server)
                except AttributeError:
                    Logger.debug('App : Function not found or not implemented')
                continue
        except KeyError:
            Logger.debug(
                f'KeyError : {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )
        for clock_key in self.running_clocks.keys():
            if server.name in clock_key:
                self.cancel_clock(clock_key)

    def check_running_os(self, *args):
        if platform.system() == 'Linux':
            return True
        if platform.system() == 'Windows':
            return False
        else:
            return False

    def request_visor_acesso(self, server: ServidorSAGE) -> None:
        Logger.info(f'VisorAcesso : Requesting VisorAcesso at {server.name}')
        server.visor_acesso = True

        if server.conn_status:
            server.conn_supervision = True
        if server.gcd:
            server.gcd_supervision = True

        if server.async_client is None:
            server.build_async_ssh_client()

        ak.start(
            self.async_cmd_with_args(
                server.async_client.open_visor_acesso,
                self.visor_acesso_exit,
                server,
            )
        )
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.open_visor_acesso()
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

        self.autoswitch_choose_server()

    def visor_acesso_exit(self, close_log: str, server: ServidorSAGE, *args):
        Logger.info(f'VisorAcesso : Exit VisorAcesso at {server.name}')

        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.close_visor_acesso()
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

        server.visor_acesso = False
        server.conn_supervision = False
        server.gcd_supervision = False
        self.autoswitch_choose_server()

    def cancel_visor_acesso(self, server: ServidorSAGE) -> None:
        Logger.info(f'VisorAcesso : Canceling VisorAcesso at {server.name}')
        ak.start(
            self.async_cmd_with_args(
                server.async_client.close_visor_acesso,
                self.visor_acesso_exit,
                server,
            )
        )
        self.autoswitch_choose_server()

    def request_syslog(self, server: ServidorSAGE) -> None:
        Logger.info(f'App : Requesting {server.name} SysLog')

        if server.async_client is None:
            server.build_async_ssh_client()

        ak.start(
            self.async_cmd_with_args(
                server.async_client.open_syslog, self.syslog_exit, server
            )
        )
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.open_syslog()
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def syslog_exit(self, *args) -> None:
        Logger.info('App : Syslog closed.')

    def request_remote_terminal(self, server: ServidorSAGE) -> None:
        Logger.info(f'App : Requesting {server.name} Remote Terminal')

        if server.async_client is None:
            server.build_async_ssh_client()

        ak.start(
            self.async_cmd_with_args(
                server.async_client.open_remote_terminal,
                self.remote_terminal_exit,
                server,
            )
        )
        try:
            for widget in self.widgets[server.name].values():
                try:
                    widget.open_syslog()
                except AttributeError:
                    continue
        except KeyError:
            print(
                f'KeyError {server.name} is not SAGE_1, SAGE_2, THIN_1 or THIN_2'
            )

    def remote_terminal_exit(self, *args) -> None:
        Logger.info('App : Remote Terminal closed.')

    def start_ping_test(self, server: ServidorSAGE, card) -> None:
        Logger.info('App : Ping test started.')
        Logger.info(f'App : Ping test target: {server.host}.')

        card.reset_icon()
        card.toggle_spinner()

        ak.start(
            self.async_cmd_with_args(
                server.ping_test, self.ping_test_result, server, card
            )
        )

    def ping_test_result(self, result, server, card, *args):
        log_result = 'success' if result else 'fail'
        Logger.info(
            f'App : Ping test result {log_result} for destination {server.host}'
        )
        card.toggle_spinner()
        card.define_icon(result)

    def start_ping_test_remote(
        self, target_ip: str, server: ServidorSAGE, card
    ) -> None:
        Logger.info('App : Ping test started.')
        Logger.info(
            f'App : Ping test from {server.host} targeting: {target_ip} .'
        )

        server.define_target_for_ping(target_ip)

        ak.start(
            self.async_cmd_with_args(
                server.exec_ping, self.ping_test_remote_result, server, card
            )
        )

    def ping_test_remote_result(
        self, result: bool, server: ServidorSAGE, card, *args
    ):
        log_result = 'success' if result else 'fail'
        Logger.info(
            f'App : Ping test result {log_result} for destination {server.target_for_ping}'
        )
        card.toggle_spinner()
        card.define_icon(result)

    def autoswitch_validation(self) -> bool:
        sage1_ok = self.SAGE_1.conn_status and self.SAGE_1.gcd
        sage2_ok = self.SAGE_2.conn_status and self.SAGE_2.gcd
        return sage1_ok and sage2_ok

    def autoswitch_toggle(self) -> bool:
        if self.autoswitch_active:
            self.autoswitch_active = not self.autoswitch_active
        else:
            self.autoswitch_active = self.autoswitch_validation()

        self.autoswitch_save_config()
        return self.autoswitch_active

    def autoswitch_choose_server(self) -> None:
        _visor_sage1 = self.SAGE_1.visor_acesso
        _visor_sage2 = self.SAGE_2.visor_acesso

        if _visor_sage1 and not _visor_sage2:
            self.autoswitch_target = self.SAGE_2
            self.autoswitch_current = self.SAGE_1
            return

        if not _visor_sage1 and _visor_sage2:
            self.autoswitch_target = self.SAGE_1
            self.autoswitch_current = self.SAGE_2
            return

        self.autoswitch_target = None
        self.autoswitch_current = None

    def autoswitch_target_ok(self) -> bool:
        if self.autoswitch_target == None:
            return False
        if self.autoswitch_target == self.SAGE_1:
            return (
                self.SAGE_1.conn_status
                and self.SAGE_1.gcd
                and not self.SAGE_1.visor_acesso
            )
        if self.autoswitch_target == self.SAGE_2:
            return (
                self.SAGE_2.conn_status
                and self.SAGE_2.gcd
                and not self.SAGE_2.visor_acesso
            )

    def autoswitch_update_connection(
        self, data: bool, server: ServidorSAGE
    ) -> None:
        _previous_value = server.conn_supervision
        _visor_open = server.visor_acesso

        # print(f'autoswitch_update_connection - prev: {_previous_value} - data: {data} - visor: {_visor_open}')
        if self.autoswitch_active:
            _drop_conn = _previous_value and not data
            if _drop_conn and _visor_open:
                self.autoswitch_trigger()

    def autoswitch_update_gcd_state(
        self, data: bool, server: ServidorSAGE
    ) -> None:

        _previous_value = server.gcd_supervision
        _visor_open = server.visor_acesso
        # print(f'autoswitch_update_gcd_state - prev: {_previous_value} - data: {data} - visor: {_visor_open}')

        if self.autoswitch_active:
            _drop_gcd = _previous_value and not data
            if _drop_gcd and _visor_open:
                self.autoswitch_trigger()

    def autoswitch_switch_VisorAcesso(self) -> None:
        self.cancel_visor_acesso(self.autoswitch_current)
        self.request_visor_acesso(self.autoswitch_target)

    def autoswitch_trigger(self) -> None:
        Logger.info('AutoSwitch : Triggered')

        var = self.autoswitch_target_ok()
        # print(f'autoswitch_target_ok = {var}')
        # print(f'autoswitch_target = {self.autoswitch_target}')
        # print(f'autoswitch_current = {self.autoswitch_current}')
        # print(f'autoswitch_sage1 visor acesso = {self.SAGE_1.visor_acesso}')
        # print(f'autoswitch_sage2 visor acesso = {self.SAGE_2.visor_acesso}')
        if var:
            self.autoswitch_switch_VisorAcesso()
