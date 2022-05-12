import asynckivy as ak
from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRoundFlatButton


class ConnectionState(MDBoxLayout, CommonFeatures):
    target = ObjectProperty(ServidorSAGE)
    conn_state_txt = StringProperty('Desconectado')
    spinner = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name][f'CONN_STATE_{id(self)}'] = self

        return super().on_kv_post(base_widget)

    def connect(self, *args) -> None:
        if self.target.host == 'xxx.xxx.xxx.xxx':
            self._snackbar_error('Configure um IP valido')

        else:
            self.spinner = True
            self.app.connect_to_server(self.target)

    def disconnect(self, *args) -> None:
        self.app.disconnect(self.target)

        self.ids.btn_container.clear_widgets()
        self.ids.btn_container.add_widget(
            ConnectionButton(on_press=self.connect)
        )

    def update_connection(self, data: bool) -> None:
        self.spinner = False

        if data:
            self.positive_conn()
        else:
            self.negative_conn()

    def positive_conn(self):
        self.conn_state_txt = 'Conectado'

        self.ids.btn_container.clear_widgets()
        self.ids.btn_container.add_widget(
            DisconnectionButton(on_press=self.disconnect)
        )

    def negative_conn(self):
        self.conn_state_txt = 'Desconectado'

        self._snackbar_error('Falha na Conexao')


class ConnectionButton(MDFillRoundFlatButton):
    ...


class DisconnectionButton(MDRoundFlatButton):
    ...
