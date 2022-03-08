import asynckivy as ak
from auxiliary.common import CommonFeatures
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.spinner import MDSpinner
from widgets.card.proccess import ProccessCard
from widgets.card.serverconfig import ConfigCard


class CommandCard(MDCard, CommonFeatures):
    image = StringProperty('')
    title = StringProperty('Action')
    btn_icon = StringProperty('centos')
    btn_text = StringProperty('Executar')
    server_target = ObjectProperty(None, allownone=True)
    release_function = DictProperty()

    screen = None

    def _get_screen(self) -> None:
        screen = self.parent.parent.parent
        self.screen = screen

    # Actions
    def open_visor_acesso(self, args: dict) -> None:
        print(
            f'Comando para abrir VisorAcesso no Servidor {self.server_target.host}'
        )

    def get_proccess_running_in_server(self, args: dict):
        self._get_screen()
        self.screen.add_widget(ProccessCard())
        if self.server_target.gcd:
            self._snackbar_error(
                f'Abrir Card com Processos : GCD - {self.server_target.gcd}'
            )
        else:
            self._snackbar_error(
                f'Abrir Card com Processos : GCD - {self.server_target.gcd}'
            )

    def execute_remote_command(self, args: dict):
        self._get_screen()
        print(f'Executar comando no Servidor {self.server_target.host}')
        print(args)

    # Future Responses
    def reaction_get_proccess_running_in_server(self, data: dict) -> None:
        pass
