from auxiliary.kvlang import string_builder
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from widgets.screen.srv1screen import Srv1Screen

# Build kv string from kv files
KV = string_builder()


class FernApp(MDApp):
    CONFIG_PATH = './Fern/config.json'
    CONFIG_STORAGE = JsonStore(CONFIG_PATH)

    SAGE_1 = ServidorSAGE('127.0.0.1')
    SAGE_2 = ServidorSAGE('127.0.0.1')

    RUNNING_CLOCK = {}

    def on_start(self):
        # Config
        self.title = 'Zugriff'
        self.setup()

        return super().on_start()

    def setup(self) -> None:
        try:
            self.SAGE_1.set_config(self.CONFIG_STORAGE.get('sage1'))
            self.SAGE_2.set_config(self.CONFIG_STORAGE.get('sage2'))
        except KeyError:
            print('WARNING: Configuration file incomplete.')

    def build(self):
        # colors
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_palette = 'Cyan'
        self.theme_cls.primary_hue = '700'

        self.success_color = self.theme_cls.colors['Green']['400']
        self.failure_color = self.theme_cls.colors['Red']['400']

        return Builder.load_string(KV)


if __name__ == '__main__':
    FernApp().run()
