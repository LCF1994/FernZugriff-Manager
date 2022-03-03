from kivymd.uix.floatlayout import MDFloatLayout
from widgets.card.serverconfig import ConfigCard
from widgets.connectionstate import ConnectionState


class Srv1Screen(MDFloatLayout):
    def open_card(self):
        self.parent.add_widget(ConfigCard())
