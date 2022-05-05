from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty,
    DictProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

# from kivymd.uix.spinner import MDSpinner
from widgets.card.process import ProcessCard

# from widgets.card.serverconfig import ConfigCard


class CommandCard(MDCard, CommonFeatures):
    name = StringProperty('')

    image = StringProperty('')
    title = StringProperty('Action')
    btn_icon = StringProperty('centos')
    btn_text = StringProperty('Executar')

    btn_disable = BooleanProperty(True)

    target = ObjectProperty(ServidorSAGE)

    release_function = DictProperty()

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name][
            f'COMMAND_CARD_{self.name.upper()}'
        ] = self

        self.screen = self.parent.parent.parent
        return super().on_kv_post(base_widget)

    def update_connection(self, conn_state: bool) -> None:
        self.btn_disable = not conn_state

    # Actions
    def open_visor_acesso(self) -> None:
        self.btn_disable = True
        Logger.info('VisorAcesso : Start request avaliation')
        result = self.app.check_running_os(self.target)
        if result:
            self._snackbar_error('Disponivel apenas no Linux.')

    def open_process_card(self):
        self.screen.add_widget(
            ProcessCard(
                target=self.target,
            )
        )

        self.app._on_open_process_card(self.target)

    def execute_remote_command(self):
        print(f'Executar comando no Servidor {self.target.host}')
