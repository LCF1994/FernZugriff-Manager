import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar


class ConnectionState(MDBoxLayout):
    conn_state = StringProperty('Offline')
    target = ObjectProperty(None)
    spinner = BooleanProperty(False)

    def _snackbar_error(self, message: str) -> None:
        Snackbar(
            text=f'[color=#ee3434]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    async def async_cmd(self, target: ServidorSAGE) -> None:
        result = await ak.run_in_thread(target.connect)
        self._connection_result(result)

    def _connection_result(self, data: bool) -> None:
        self.spinner = False
        print(f'Dados recebidos: {data}')

        if data is True:
            self.conn_state = 'Online'
        else:
            self._snackbar_error('Falha na Conexao')

    def connect(self) -> None:
        if self.target.host == '127.0.0.1':
            self._snackbar_error('Configure um IP valido')

        else:
            print(f'Target IP: {self.target.host}')

            self.spinner = True

            ak.start(self.async_cmd(self.target))
