import asynckivy as ak
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import (
    ColorProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class ServerDetails(MDBoxLayout):
    os = StringProperty('linux')
    hostname = StringProperty('Host')
    version = StringProperty('xx-xx')
    database = StringProperty('undefined')
    dbtype = StringProperty('undefined')
    gcd = StringProperty('desativado')
    gcd_color = ColorProperty([0, 0, 1, 1])
    server_hot = StringProperty('stand by')
    server_hot_color = ColorProperty([0, 0, 1, 1])
    sound = StringProperty('undefined')
    redundancy = StringProperty('undefined')
    network_node = StringProperty('undefined')

    target = ObjectProperty(ServidorSAGE)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name][f'DB_DETAILS_{id(self)}'] = self
        return super().on_kv_post(base_widget)

    # Rotines for Connection
    def update_connection(self, connected: bool, *args) -> None:
        if connected is True:
            self.update_data(self.target)

    def update_data(self, server: ServidorSAGE) -> None:
        ak.start(self._request_data(server))

    async def _request_data(self, server: ServidorSAGE) -> None:
        data = await ak.run_in_thread(server.get_var)
        self._update_widget_data(data)

    def _update_widget_data(self, data: dict) -> None:
        self.os = data['CPU']
        self.hostname = data['HOST']
        self.version = data['VERSAO']
        self.database = data['BASE']
        self.gcd = 'ativo' if data['GCD'] else 'desativado'
        self.gcd_color = (
            self.app.success_color if data['GCD'] else self.app.failure_color
        )
        self.server_hot = 'hot' if data['SERVER_HOT'] else 'stand by'
        self.server_hot_color = (
            self.app.failure_color
            if data['SERVER_HOT']
            else self.app.neutral_color
        )
        self.dbtype = data['MODELO']
        self.sound = data['SOM']
        self.redundancy = data['DIFUSAO']
        self.network_node = data['LOCAL']

    # Rotines for gcd state
    def update_gcd_state(self, gcd_state: bool, *args) -> None:
        if gcd_state is True:
            self.gcd_running()
        else:
            self.gcd_stoped()

    def gcd_running(self) -> None:
        self.gcd = 'ativo'
        self.gcd_color = self.app.success_color

    def gcd_stoped(self) -> None:
        self.gcd = 'desativado'
        self.gcd_color = self.app.failure_color

    def update_server_hot(self, server_hot: bool, *args) -> None:
        if server_hot is True:
            self.server_hot = 'HOT'
            self.server_hot_color = self.app.failure_color
        else:
            self.server_hot = 'stand by'
            self.server_hot_color = self.app.neutral_color


class Item(MDBoxLayout):
    title = StringProperty('ITEM')
    value = StringProperty('undefined')
    theme = OptionProperty(
        'Custom',
        options=[
            'Primary',
            'Secondary',
            'Hint',
            'Error',
            'Custom',
            'ContrastParentBackground',
        ],
        allownone=True,
    )
    color = ColorProperty([1, 1, 1, 1])
