from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
# from auxiliary.servidor_paramiko import ServidorSAGE
from auxiliary.servidor_asyncssh import ServidorSAGE
from kivymd.uix.snackbar import Snackbar
import asynckivy as ak
import asyncio, asyncssh, sys


class ConnectionState(MDBoxLayout):

    def _snackbar_error(self, message) -> None:
        Snackbar(
               text=f'[color=#ee3434]{message}[/color]',
               snackbar_x='10dp',
               snackbar_y='10dp',
               size_hint_x=0.95,
           ).open()

    def connect(self, target:ServidorSAGE, app) -> bool:
        async def async_cmd(self, target):
            try:
                r = await ak.run_in_thread(target.exec_cmd('whoami'))
                print(r)
                return r

            except (OSError, asyncssh.Error) as exc:
                sys.exit('SSH connection failed: ' + str(exc))

        print(target)

        if target.host == '127.0.0.1':
            self._snackbar_error('Configure um IP valido')
            return False

        else:
            print(f'Target IP: {target.host}')

            self.ids.conn_spinner.active = True
        
            retorno = ak.start(async_cmd(self, target))

            self.ids.conn_spinner.active = False


            #self.remove_widget(self.ids.conn_btn)
        #self.add_widget(RefreshButton())


class RefreshButton(MDIconButton):
    def refresh(self):
        current_text = self.parent.ids.text.text

        if current_text == 'Offline':
            self.parent.ids.text.text = 'Online'
        else:
            self.parent.ids.text.text = 'Offline'
