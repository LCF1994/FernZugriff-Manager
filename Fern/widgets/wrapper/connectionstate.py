import asynckivy as ak
from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton


class ConnectionState(MDBoxLayout, CommonFeatures):
    conn_state_txt = StringProperty('Offline')
    target = ObjectProperty(ServidorSAGE)
    spinner = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['CONN_STATE'] = self

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

        if data is True:
            self.positive_conn()
        else:
            self.negative_conn()

    def positive_conn(self):
        self.conn_state_txt = 'Online'

        self.ids.btn_container.clear_widgets()
        self.ids.btn_container.add_widget(
            DisconnectionButton(on_press=self.disconnect)
        )

    def negative_conn(self):
        self.conn_state_txt = 'Offline'
        self.spinner = False

        self._snackbar_error('Falha na Conexao')


class ConnectionButton(MDFillRoundFlatButton):
    ...


class DisconnectionButton(MDRectangleFlatButton):
    ...
