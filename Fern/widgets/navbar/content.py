from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer


class MyNavDrawer(MDNavigationDrawer):
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.navbar = self
        return super().on_kv_post(base_widget)

    def on_enter(self):
        self.app.navlist.clear_widgets()
        for item in self.app.NAV_ITENS.values():
            self.app.navlist.add_widget(
                NavItem(
                    text=item['text'], icon=item['icon'], screen=item['screen']
                )
            )
        return super().on_enter()


class NavList(MDList):
    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.navlist = self
        return super().on_kv_post(base_widget)


class NavItem(OneLineIconListItem):
    icon = StringProperty('')
    text = StringProperty('')
    screen = StringProperty('')
