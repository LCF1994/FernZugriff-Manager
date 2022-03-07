from auxiliary.kvlang import string_builder
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from widgets.screen.srv1screen import Srv1Screen

# Build kv string from kv files
KV = string_builder()


class FernApp(MDApp):

    SAGE_1 = ServidorSAGE('127.0.0.1')
    SAGE_2 = ServidorSAGE('127.0.0.1')

    RUNNING_CLOCK = []

    def on_start(self):
        # For scheduling events on_start from config File

        # if self.SVR1_CONFIGURED:
        #     self.GET_GCD_RUNNING = Clock.schedule_interval(self.test, 1)
        return super().on_start()

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
