from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard


class ServerStatus(MDCard):
    server = ObjectProperty(ServidorSAGE)
    server_name = StringProperty('SAGE X')
    gcd_status = StringProperty('Desativado')
    gcd_status_color = ColorProperty([1, 1, 0, 1])
    server_hot = StringProperty('Stand by')
    server_hot_color = ColorProperty([1, 1, 0, 1])
    visor_acesso = StringProperty('Fechado')

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.server.name][f'SERVER_STATUS_{id(self)}'] = self

        try:
            self.server_name = self.server.name.replace('_', ' ')
        except AttributeError:
            Logger.debug('App : Error on kv post')

        return super().on_kv_post(base_widget)

    def open_dashboard(self) -> None:
        screen = self.server.name.replace('_', '').lower()
        self.app.screen_manager.current = screen

    def update_gcd_state(self, status: bool, *args) -> None:
        if status is True:
            self.gcd_status = 'Ativado'
            self.gcd_status_color = self.app.success_color
        else:
            self.gcd_status = 'Desativado'
            self.gcd_status_color = self.app.failure_color

    def update_server_hot(self, server_hot: bool, *args) -> None:
        if server_hot is True:
            self.server_hot = 'HOT'
            self.server_hot_color = self.app.failure_color
        else:
            self.server_hot = 'Stand by'
            self.server_hot_color = self.app.neutral_color

    class ItemWrapper(MDBoxLayout):
        title = StringProperty('title')
        value = StringProperty('value')
        color = ColorProperty([1, 1, 1, 1])
