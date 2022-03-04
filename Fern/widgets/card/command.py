from kivy.properties import ObjectProperty, Property, StringProperty
from kivymd.uix.card import MDCard


class CommandCard(MDCard):
    image = StringProperty('')
    title = StringProperty('Action')
    btn_icon = StringProperty('centos')
    btn_text = StringProperty('Executar')
    server_target = ObjectProperty(None, allownone=True)
    release_function = Property(None)

    def abre_visor_acesso(self):
        print(
            f'Comando para abrir VisorAcesso no Servidor {self.server_target.host}'
        )

    def get_server_info(self):
        print(
            f'Comando receber informações do Servidor {self.server_target.host}'
        )

    def executar_remote_command(self):
        print(f'Executar comando no Servidor {self.server_target.host}')
