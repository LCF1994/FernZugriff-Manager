import os

os.environ['KCFG_GRAPHICS_RESIZABLE'] = '0'
os.environ['KCFG_GRAPHICS_ALLOW_SCREENSAVER'] = '0'

from auxiliary.extentions import Extentions
from auxiliary.kvlang import string_builder
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from widgets.navbar.content import MyNavDrawer
from widgets.screen.screen_about import AboutScreen
from widgets.screen.screen_home import HomeScreen
from widgets.screen.screen_manager import MyScreenManager
from widgets.screen.screen_sage import ScreenSage1, ScreenSage2
from widgets.screen.screen_tools import ToolsScreen

# Build kv string from kv files
KV = string_builder('./Fern/assets/kv/')

CONFIG_PATH = './Fern/config.json'


class FernApp(MDApp, Extentions):
    SAGE_1 = ServidorSAGE('SAGE_1', 'xxx.xxx.xxx.xxx')
    SAGE_2 = ServidorSAGE('SAGE_2', 'xxx.xxx.xxx.xxx')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = JsonStore(CONFIG_PATH)

        self.set_config_up()

    def set_config_up(self) -> None:
        try:
            self.SAGE_1.set_config(self.storage.get('SAGE_1'))
            self.SAGE_2.set_config(self.storage.get('SAGE_2'))

            Logger.info('Settings: Configuration file loaded')
        except KeyError:
            Logger.warning('Settings: Configuration file incomplete')

    def define_theme(self) -> None:
        # colors
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.primary_hue = '400'

        self.theme_cls.primary_color

        self.success_color = self.theme_cls.colors['LightGreen']['A400']
        self.neutral_color = self.theme_cls.text_color
        self.failure_color = self.theme_cls.colors['Red']['A700']

    def build(self):
        self.title = 'Zugriff'

        self.define_theme()

        return Builder.load_string(KV)


if __name__ == '__main__':
    FernApp().run()
