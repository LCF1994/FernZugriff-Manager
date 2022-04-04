import re

from auxiliary.common import CommonCard, CommonFeatures
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.card import MDCard


class ConfigCard(MDCard, CommonFeatures, CommonCard):
    target = ObjectProperty(None)
    srv_name = StringProperty('SAGE ')

    def cancel_button(self) -> None:
        self.close_card()

    def save_button(self) -> None:
        data = {
            'host': self.ids.server_ip.text,
            'username': self.ids.username.text
            if self.ids.username.text != ''
            else 'sagetr1',
            'password': self.ids.password.text
            if self.ids.password.text != ''
            else 'sagetr1',
            'port': self.ids.port_number.text
            if self.ids.port_number.text != ''
            else 22,
        }
        print(data)

        if self._validate_server_ip() and self._validate_ssh_port():
            self._save_data(data)
            self.close_card()

    def _validate_server_ip(self) -> bool:
        if not self.ids.server_ip.text:
            self._snackbar_error('Insira um IP para o Servidor !')
            return False
        return True

    def _validate_ssh_port(self) -> bool:
        if self.ids.port_number.text:
            try:
                port_value = int(self.ids.port_number.text)
                return 0 <= port_value <= 65_535
            except (ValueError, TypeError):
                self._snackbar_error(
                    'Porta invalida ! - Insira um numero de 0 a 65,535'
                )
                return False
        else:
            return True

    def _save_data(self, data) -> None:

        self.parent.ids.srv_title.server_ip = data['host']

        # update server data
        self.target.set_host(data['host'])
        self.target.username = data['username']
        self.target.password = data['password']
        self.target.port = data['port']

        print('Dados salvos')
        print(f'host:{self.target.host}')
