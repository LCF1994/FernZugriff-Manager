from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar


class ConfigCard(MDCard):
    def close_card(self) -> None:
        self.parent.remove_widget(self)

    def check_card_focus(self, args) -> None:
        x, y = args[1].pos

        # check unfocus
        if not self.collide_point(x, y):
            self.parent.remove_widget(self)

    def cancel_button(self) -> None:
        self.close_card()

    def save_button(self, app) -> None:
        data = {
            'server_ip': self.ids.server_ip.text,
            'username': self.ids.username.text
            if not self.ids.username.text
            else 'sagetr1',
            'password': self.ids.password.text
            if not self.ids.password.text
            else 'sagetr1',
            'ssh_port': self.ids.port_number.text
            if not self.ids.port_number.text
            else 22,
        }
        print(data)

        if self._validate_server_ip() and self._validate_ssh_port():
            self._save_data(data, app)
            self.close_card()

    def _validate_server_ip(self) -> bool:
        if not self.ids.server_ip.text:
            Snackbar(
                text='[color=#ee3434]Insira um IP para o Servidor ![/color]',
                snackbar_x='10dp',
                snackbar_y='10dp',
                size_hint_x=0.95,
            ).open()
            return False
        return True

    def _validate_ssh_port(self) -> bool:
        if self.ids.port_number.text:
            try:
                int(self.ids.port_number.text)
                return True
            except ValueError:
                Snackbar(
                    text='[color=#ee3434]Porta invalida ! - Insira um numero de 0 a 65,535 [/color]',
                    snackbar_x='10dp',
                    snackbar_y='10dp',
                    size_hint_x=0.95,
                ).open()
            return False
        else:
            return True

    def _save_data(self, data, app) -> None:
        self.parent.ids.server_ip.text = f'    IP: {data["server_ip"]}'
