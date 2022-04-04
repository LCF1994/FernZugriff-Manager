import re

from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

IP_PATTERN = r'\d{3}'


class ServerTitle(MDBoxLayout):
    target = ObjectProperty(ServidorSAGE)
    title = StringProperty('Server XX')
    server_ip = StringProperty('xxx.xxx.xxx.xxx')

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['TITLE'] = self
        return super().on_kv_post(base_widget)

    def update_ip(self, new_ip: str, *, validation=True) -> None:
        self.server_ip = new_ip

        if validation:
            result = True
            matches = re.finditer(IP_PATTERN, new_ip)
            for match in matches:
                int_match = int(match.group())
                result = result and (int_match <= 255)

            if result is False:
                Logger.warning('App : IP received is not valid as IPV4')
                Logger.warning('App : Alias or IPV6 may not work properly')
