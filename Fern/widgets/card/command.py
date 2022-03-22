import asynckivy as ak
from auxiliary.common import CommonFeatures
from kivy.clock import Clock
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
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

        ak.start(
            self.async_cmd(
                self.server_target.get_server_proccess,
                self.reaction_get_proccess_running_in_server,
            )
        )

    def execute_remote_command(self, args: dict):
        self._get_screen()
        print(f'Executar comando no Servidor {self.server_target.host}')
        print(args)

    # Future Responses
    def reaction_get_proccess_running_in_server(self, data: list) -> None:

        self.screen.add_widget(
            ProccessCard(
                app=MDApp.get_running_app(),
                proccess_list=data,
                server_target=self.server_target,
            )
        )
