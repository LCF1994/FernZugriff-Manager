import sys

import asynckivy as ak
import asyncssh
from auxiliary.servidor_paramiko import ServidorSAGE
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

# from auxiliary.servidor_asyncssh import ServidorSAGE
from kivymd.uix.snackbar import Snackbar


class ConnectionState(MDBoxLayout):
    def _snackbar_error(self, message) -> None:
        Snackbar(
            text=f'[color=#ee3434]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    async def async_cmd(self, target):
        try:
            # result = await ak.run_in_thread(target.run_thread)
            result = await ak.run_in_thread(target.connect)
            self._success_connection(result)

        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))

    def _success_connection(self, data):
        self.ids.conn_spinner.active = False
        print(f'Dados recebidos: {data}')
        if data is True:
            self.ids.text.text = 'Online'

    def connect(self, target) -> bool:
        running_app = MDApp.get_running_app()
        print(target)
        if target == 'sage1':
            target = running_app.SAGE_1
        elif target == 'sage2':
            target = running_app.SAGE_2
        else:
            self._snackbar_error('Target Not found !')
            return False

        print(target)

        if target.host == '127.0.0.1':
            self._snackbar_error('Configure um IP valido')
            return False

        else:
            print(f'Target IP: {target.host}')

            self.ids.conn_spinner.active = True

            ak.start(self.async_cmd(target))


class RefreshButton(MDIconButton):
    def refresh(self):
        current_text = self.parent.ids.text.text

        if current_text == 'Offline':
            self.parent.ids.text.text = 'Online'
        else:
            self.parent.ids.text.text = 'Offline'
