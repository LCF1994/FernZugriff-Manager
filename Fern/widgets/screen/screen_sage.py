from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import Screen
from widgets.card.command import CommandCard
from widgets.card.serverconfig import ConfigCard
from widgets.wrapper.body import BodyContainer
from widgets.wrapper.connectionstate import ConnectionState
from widgets.wrapper.servertitle import ServerTitle


class ScreenSage1(Screen):
    server = ObjectProperty(ServidorSAGE)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        return super().on_kv_post(base_widget)

    def on_enter(self, *args):
        self.app.set_ip_on_server_title(self.server)
        return super().on_enter(*args)


class ScreenSage2(Screen):
    server = ObjectProperty(ServidorSAGE)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        return super().on_kv_post(base_widget)

    def on_enter(self, *args):
        self.app.set_ip_on_server_title(self.server)
        return super().on_enter(*args)


class ScreenSageDefault(MDFloatLayout):
    server = ObjectProperty(ServidorSAGE)
    srv_name = StringProperty('Servidor X')

    def open_card(self) -> None:
        self.add_widget(ConfigCard(server=self.server))
