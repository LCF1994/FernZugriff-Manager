from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import BooleanProperty, StringProperty, ColorProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from widgets.card.help import HelpCard

class AutoSwitch(MDFloatLayout):
    
    TEXT_AUTOSWITCH = '''
    Funcionalidade que permite a abertura automatica do Visor Acesso em caso de desconexao ou desativacao do GCD.

    Requerimentos:
     - Conexao com ambos os Servidores
     - Ambos os servidores com GCD ativo



    '''

    def open_help(self):
        self.parent.add_widget(
            HelpCard(
                title='Transferencia Automatica',
                content=self.TEXT_AUTOSWITCH
            )
        )


class SwitchButton(MDRoundFlatButton):
    text = StringProperty('Button')
    color = ColorProperty([1, 1, 1, 1])
    status = BooleanProperty(False)


    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets['SAGE_1']['AUTOSWITCH'] = self
        self.app.widgets['SAGE_2']['AUTOSWITCH'] = self

        self.text = 'Desligada'
        self.color = self.app.failure_color
        return super().on_kv_post(base_widget)
    

    def toggle(self):
        self.status = not self.status

        if self.status:
            self.text = 'Ligada'
            self.color = self.app.success_color
        else:
            self.text = 'Desligada'
            self.color = self.app.failure_color
    

