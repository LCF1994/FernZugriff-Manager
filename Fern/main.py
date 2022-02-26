from auxiliary.kvlang import string_builder
from kivy.lang import Builder
from kivymd.app import MDApp
#from servidor import ServidorSAGE
from servidor_paramiko import ServidorSAGE
from widgets.card.serverconfig import ConfigCard
from widgets.connectionstate import ConnectionState

# Build kv string from kv files
KV = string_builder()


class FernApp(MDApp):
    sage1 = ServidorSAGE('127.0.0.1')

    def open_card(self, screen):
        screen.add_widget(ConfigCard())

    def build(self):
        # Config
        self.title = 'Zugriff'

        # colors
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_palette = 'Cyan'
        self.theme_cls.primary_hue = '700'

        self.success_color = self.theme_cls.colors['Green']['400']
        self.failure_color = self.theme_cls.colors['Red']['400']

        # Build
        return Builder.load_string(KV)


if __name__ == '__main__':
    FernApp().run()
