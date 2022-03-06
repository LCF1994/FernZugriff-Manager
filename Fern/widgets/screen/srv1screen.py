from kivy.properties import ObjectProperty
from kivymd.uix.screen import Screen
from widgets.card.command import CommandCard
from widgets.card.serverconfig import ConfigCard
from widgets.wrapper.body import BodyContainer
from widgets.wrapper.connectionstate import ConnectionState
from widgets.wrapper.servertitle import ServerTitle


class Srv1Screen(Screen):
    server = ObjectProperty(None)

    def open_card(self) -> None:
        self.add_widget(ConfigCard(target=self.server))
