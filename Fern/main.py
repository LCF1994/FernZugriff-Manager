import os

os.environ['KCFG_GRAPHICS_RESIZABLE'] = '0'
os.environ['KCFG_GRAPHICS_ALLOW_SCREENSAVER'] = '0'

from auxiliary.extensions import Extensions
from auxiliary.kvlang import string_builder
from auxiliary.servidor_paramiko import ServidorSAGE
from auxiliary.theming import apply_default_theme, apply_siemens_theme
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from widgets.navbar.content import MyNavDrawer
from widgets.screen.screen_about import AboutScreen
from widgets.screen.screen_autoswitch import AutoSwitchScreen
from widgets.screen.screen_home import HomeScreen, SiemensHomeScreen
from widgets.screen.screen_manager import MyScreenManager
from widgets.screen.screen_pingtest import PingTestScreen
from widgets.screen.screen_sage import ScreenSage1, ScreenSage2

# Build kv string from kv files
# KV = string_builder()

CONFIG_PATH = 'config.json'

try:
    import pyi_splash

    pyi_splash.close()
except ModuleNotFoundError:
    pass


class FernApp(MDApp, Extensions):
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

            self.autoswitch_active = self.storage.get('app')['autoswitch']
            # print(self.storage.get('app'))

            Logger.info('Settings: Configuration file loaded')
        except KeyError:
            Logger.warning('Settings: Configuration file incomplete')

    def build(self):
        self.title = 'Thin Client Dashboard'
        self.icon = self.resource_path('images/sie-favicon.png')

        # apply_default_theme(self)
        apply_siemens_theme(self)

        return Builder.load_string(string_builder(self.resource_path('kv')))


if __name__ == '__main__':
    FernApp().run()
