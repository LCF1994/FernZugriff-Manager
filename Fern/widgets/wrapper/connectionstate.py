import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar


class ConnectionState(MDBoxLayout):
    conn_state = StringProperty('Offline')
    target = ObjectProperty(None)
    spinner = BooleanProperty(False)

    app = None
    screen_body = None
    clock_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clock_list.extend([
            self._update_conn_state,
            self._update_gcd_state,
            self._update_charts_value,
        ])

    def _snackbar_error(self, message: str) -> None:
        Snackbar(
            text=f'[color=#ee3434]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    def _clear_clocks(self) -> None:
        for clock in self.app.RUNNING_CLOCK:
            clock.cancel()

    def connect(self) -> None:
        self.app = MDApp.get_running_app()
        self.screen_body = self.parent.parent.ids.body_container

        if self.target.host == '127.0.0.1':
            self._snackbar_error('Configure um IP valido')

        else:
            print(f'Target IP: {self.target.host}')
            self.spinner = True
            ak.start(self.async_cmd(self.target))

    async def async_cmd(self, target: ServidorSAGE) -> None:
        result = await ak.run_in_thread(target.connect)
        self._connection_result(result)

    def _connection_result(self, data: bool) -> None:
        self.spinner = False
        print(f'Dados recebidos: {data}')

        if data is True:
            self.conn_state = 'Online'
            self.screen_body.ids.cover_conn.message = ''
            self.screen_body.ids.cover_conn.opacity = 0

            self.screen_body.ids.details.update_data(self.target)
            self.run_clock_list()

            # alterar para dict, possibilitando o cancelamento de rotinas especificas
            self.app.RUNNING_CLOCK = {
                'connection': Clock.schedule_interval(self._update_conn_state, 15),
                'gcd': Clock.schedule_interval(self._update_gcd_state, 30),
                'performance': Clock.schedule_interval(self._update_charts_value, 10), 
            }
            
        else:
            self.conn_state = 'Offline'
            self.screen_body.ids.cover_conn.message = 'Not Connected'
            self.screen_body.ids.cover_conn.opacity = 0.9

            self._clear_clocks()
            self._snackbar_error('Falha na Conexao')

    def run_clock_list(self, *args):
        for function in self.clock_list:
            function()

    # functions for connection - clock event
    def _update_conn_state(self, *args):
        print('Checking Connection State ...')
        ak.start(self._await_conn_verification())

    async def _await_conn_verification(self):
        result = await ak.run_in_thread(self.target.check_connection)
        self._conn_verifcation_result(result)

    def _conn_verifcation_result(self, new_conn_state):
        print(f'Checking Connection State: {new_conn_state} - Done')
        if not new_conn_state:
            self.conn_state = 'Offline'


    # functions for gcd - clock event
    def _update_gcd_state(self, *args):
        print('Checking GCD State ...')
        ak.start(self._await_gcd_verification())

    async def _await_gcd_verification(self):
        new_gcd_state = await ak.run_in_thread(self.target.check_gcd_running)
        self._gcd_verifcation_result(new_gcd_state)

    def _gcd_verifcation_result(self, new_gcd_state):
        print(f'Checking GCD State: {new_gcd_state} - Done')
        if not new_gcd_state:
            self.screen_body.ids.details.gcd = 'desativado'
            self.screen_body.ids.cover_chart.message = 'GCD Desativado'
            self.screen_body.ids.cover_chart.opacity = .5
            print('GCD Desativado')
        else:
            self.screen_body.ids.details.gcd = 'ativo'
            self.screen_body.ids.cover_chart.message = ''
            self.screen_body.ids.cover_chart.opacity = 0
            print('GCD ativo')

    # functions for update charts - clock event
    def _update_charts_value(self, *args) -> None:
        if self.target.gcd:
            print('Requesting Charts Update ...')
            ak.start(self._await_chart_data_request())
        else:
            print('GCD not running')

    async def _await_chart_data_request(self) -> None:
        data_received = await ak.run_in_thread(self.target.get_performance)
        self._update_charts_value_with_data_received(data_received)

    def _update_charts_value_with_data_received(self, data_received:dict) -> None:
        print(f'Requesting Charts Update: {data_received} - Done')

        self.screen_body.ids.grid_chart.cpu= data_received['cpu']
        self.screen_body.ids.grid_chart.memory= data_received['memory']
        self.screen_body.ids.grid_chart.disk_sage= data_received['disk_sage']
        self.screen_body.ids.grid_chart.disk_arqs= data_received['disk_arqs']
        self.screen_body.ids.grid_chart.disk_logs= data_received['disk_logs']
