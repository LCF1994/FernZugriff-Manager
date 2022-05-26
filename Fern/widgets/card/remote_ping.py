from http import server

from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout


class RemotePingCard(MDCard):
    server = ObjectProperty(ServidorSAGE)
    server_name = StringProperty('SAGE X')
    ping_btn_disabled = BooleanProperty(True)

    check_icon = StringProperty('')
    check_color = ColorProperty([1, 1, 1, 1])
    spinner = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.server.name][f'REMOTE_PING_{id(self)}'] = self

        try:
            self.server_name = self.server.name.replace('_', ' ')
        except AttributeError:
            Logger.debug('App : Error on kv post')

        return super().on_kv_post(base_widget)

    def update_connection(self, data: bool, *args) -> None:
        self.ping_btn_disabled = not data

    def toggle_spinner(self) -> None:
        self.spinner = not self.spinner

    def define_icon(self, result: bool) -> None:
        if result:
            self.check_color = self.app.success_color
            self.check_icon = 'check'
        else:
            self.check_color = self.app.failure_color
            self.check_icon = 'close'

    def reset_icon(self) -> None:
        self.check_icon = ''

    def get_ip_from_text(self) -> str:
        for child in self.children:
            if isinstance(child, MyIpInput):
                return child.ids.text_field.text

    def ping_request(self) -> None:
        self.reset_icon()
        self.toggle_spinner()
        target_ip = self.get_ip_from_text()
        self.app.start_ping_test_remote(target_ip, self.server, self)


class MyIpInput(MDRelativeLayout):
    check_icon = StringProperty('')
    check_color = ColorProperty([1, 1, 1, 1])
    spinner = BooleanProperty(False)
