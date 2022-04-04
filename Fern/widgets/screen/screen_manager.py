from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


class MyScreenManager(ScreenManager):
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.screen_manager = self
        return super().on_kv_post(base_widget)
