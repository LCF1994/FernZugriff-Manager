from auxiliary.common import CommonCard, CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard


class ConfigCard(MDCard, CommonFeatures, CommonCard):
    server = ObjectProperty(ServidorSAGE)
    server_name = StringProperty('SAGE ')

    server_ip = StringProperty('')
    username = StringProperty('')
    password = StringProperty('')
    port_number = StringProperty('')

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.server_name = self.server.name.replace('_', ' ')
        self.server_ip = self.server.host
        # self.username =    self.server.username
        # self.password =    self.server.password
        # self.port_number = str(self.server.port)
        return super().on_kv_post(base_widget)

    def cancel_button(self) -> None:
        self.close_card()

    def save_button(self) -> None:
        data = {
            'host': self.server_ip,
            'username': self.username if self.username != '' else 'sagetr1',
            'password': self.password if self.password != '' else 'sagetr1',
            'port': int(self.port_number) if self.port_number != '' else 22,
        }

        if self._validate_server_ip() and self._validate_ssh_port():
            self._save_data(data)
            self.close_card()

    def _validate_server_ip(self) -> bool:
        if not self.server_ip:
            self._snackbar_error('Insira um IP para o Servidor !')
            return False
        return True

    def _validate_ssh_port(self) -> bool:
        if self.port_number:
            try:
                port_value = int(self.port_number)
                return 0 <= port_value <= 65_535
            except (ValueError, TypeError):
                self._snackbar_error(
                    'Porta invalida ! - Insira um numero de 0 a 65,535'
                )
                return False
        else:
            return True

    def _save_data(self, data) -> None:
        self.server.host = data['host']
        self.server.username = data['username']
        self.server.password = data['password']
        self.server.port = data['port']

        self.app.save_config(self.server)
        self.app.set_ip_on_server_title(self.server)
