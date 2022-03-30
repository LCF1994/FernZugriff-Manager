from kivy.properties import ObjectProperty
from kivymd.uix.screen import Screen
from widgets.card.command import CommandCard
from widgets.card.serverconfig import ConfigCard
from widgets.wrapper.body import BodyContainer
from widgets.wrapper.connectionstate import ConnectionState
from widgets.wrapper.servertitle import ServerTitle


class Srv1Screen(Screen):
    server = ObjectProperty(None)
    app = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        return super().on_kv_post(base_widget)

    def on_pre_enter(self, *args):
        # if server IP valid
        # app -> connect to server
        print('Pre Enter on Screen')
        return super().on_enter(*args)

    def open_card(self) -> None:
        self.add_widget(ConfigCard(target=self.server))
