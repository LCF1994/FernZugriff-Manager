from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDRoundFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from widgets.card.help import HelpCard


class AutoSwitch(MDFloatLayout):

    TEXT_AUTOSWITCH = """
    Funcionalidade que permite a abertura automatica do Visor Acesso em caso de desconexao ou desativacao do GCD.

    Requerimentos:
     - Conexao com ambos os Servidores
     - Ambos os servidores com GCD ativo
     - Apenas um dos Visores de Acesso aberto


    """

    def open_help(self):
        self.parent.add_widget(
            HelpCard(
                title='Transferencia Automatica', content=self.TEXT_AUTOSWITCH
            )
        )


class CommonAutoSwitch:
    sage1_conn = False
    sage1_gcd_on = False
    sage2_conn = False
    sage2_gcd_on = False

    def update_connection(self, data: bool, server: ServidorSAGE) -> None:
        if '1' in server.name:
            self.sage1_conn = data
        if '2' in server.name:
            self.sage2_conn = data

    def update_gcd_state(self, data: bool, server: ServidorSAGE) -> None:
        if '1' in server.name:
            self.sage1_gcd_on = data
        if '2' in server.name:
            self.sage2_gcd_on = data

    def requiriments_validation(self) -> bool:
        sage1_ok = self.sage1_conn and self.sage1_gcd_on
        sage2_ok = self.sage2_conn and self.sage2_gcd_on

        return sage1_ok and sage2_ok


class AutoSwitchButton(MDRoundFlatButton, CommonFeatures, CommonAutoSwitch):
    text = StringProperty('Button')
    color = ColorProperty([1, 1, 1, 1])
    status = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets['SAGE_1'][f'AUTOSWITCH_{id(self)}'] = self
        self.app.widgets['SAGE_2'][f'AUTOSWITCH_{id(self)}'] = self

        self.status = self.app.autoswitch_active
        self.change_interface()

        return super().on_kv_post(base_widget)

    def toggle(self):
        toggle_request = self.app.autoswitch_toggle()

        if not self.status and not toggle_request:
            self._snackbar_error('Falha: Requerimentos nao atingidos')

        self.status = toggle_request
        self.change_interface()

    def change_interface(self) -> None:
        if self.status:
            self.text = 'Ligada'
            self.color = self.app.success_color
        else:
            self.text = 'Desligada'
            self.color = self.app.failure_color


class ManualSwitchButton(MDIconButton, CommonFeatures, CommonAutoSwitch):
    color = ColorProperty([1, 1, 1, 1])

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets['SAGE_1'][f'MANUAL_SWITCH_{id(self)}'] = self
        self.app.widgets['SAGE_2'][f'MANUAL_SWITCH_{id(self)}'] = self

        self.color = self.app.theme_cls.primary_color

        return super().on_kv_post(base_widget)

    def manual_trigger(self) -> None:
        self.app.autoswitch_trigger()
        self._snackbar_info('Troca manual de Visor requisitada')
