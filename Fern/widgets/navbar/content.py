from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer


class MyNavDrawer(MDNavigationDrawer):
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.navbar = self
        return super().on_kv_post(base_widget)


class ContentNavigationDrawer(MDBoxLayout):
    ...
