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

            self.app.RUNNING_CLOCK.append(
                Clock.schedule_interval(self._update_conn_state, 10),
                Clock.schedule_interval(self._update_gcd_state, 30),
            )
        else:
            self.conn_state = 'Offline'
            self.screen_body.ids.cover_conn.message = 'Not Connected'
            self.screen_body.ids.cover_conn.opacity = 0.9

            self._clear_clocks()
            self._snackbar_error('Falha na Conexao')

    def _update_conn_state(self, *args):
        print('Checking Connection State ...')
        ak.start(self._await_conn_verification())

    async def _await_conn_verification(self):
        result = await ak.run_in_thread(self.target.check_connection)
        self._conn_verifcation_result(result)

    def _conn_verifcation_result(self, new_conn_state):
        print('Checking Connection State: Done')
        if not new_conn_state:
            self.conn_state = 'Offline'
            self.CLOCK_CONNECTION_STATE.cancel()

    def _update_gcd_state(self, *args):
        print('Checking Connection State ...')
        ak.start(self._await_conn_verification())

    async def _await_gcd_verification(self):
        result = await ak.run_in_thread(self.target.check_gcd_running)
        self._gcd_verifcation_result(result)

    def _gcd_verifcation_result(self, new_gcd_state):
        print('Checking Connection State: Done')
        if not new_gcd_state:
            self.screen_body.ids.details.gcd = 'desativado'
            print('GCD Desativado')
        else:
            self.screen_body.ids.details.gcd = 'ativo'
            print('GCD ativo')
