from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard


class CardPingServer(MDCard):
    server = ObjectProperty(ServidorSAGE)
    title = StringProperty('Server XX')
    server_ip = StringProperty('xxx.xxx.xxx.xxx')
    check_icon = StringProperty('')
    spinner = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.title = self.server.name.replace('_', ' ')
        self.update_ip()
        return super().on_kv_post(base_widget)

    def update_ip(self) -> None:
        self.server_ip = self.server.host

    def edit_btn(self) -> None:
        print('btn edit pressed')

    def check_ping(self) -> None:
        self.app.check_ping(self.server.host, self)
