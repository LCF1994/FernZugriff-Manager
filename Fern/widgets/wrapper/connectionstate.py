import asynckivy as ak
from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class ConnectionState(MDBoxLayout, CommonFeatures):
    conn_state_txt = StringProperty('Offline')
    target = ObjectProperty(ServidorSAGE)
    spinner = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['CONN_STATE'] = self

        return super().on_kv_post(base_widget)

    def connect(self) -> None:
        if self.target.host == 'xxx.xxx.xxx.xxx':
            self._snackbar_error('Configure um IP valido')

        else:
            self.spinner = True
            self.app.connect_to_server(self.target)

    def update_connection(self, data: bool) -> None:
        self.spinner = False
        print(f'Dados recebidos: {data}')

        if data is True:
            self.positive_conn()
        else:
            self.negative_conn()

    def positive_conn(self):
        self.conn_state_txt = 'Online'
        # Must be implemented
        # change connection btn to disconnection btn

    def negative_conn(self):
        self.conn_state_txt = 'Offline'
        # Must be implemented
        # change disconnection btn to connection btn

        self._snackbar_error('Falha na Conexao')
