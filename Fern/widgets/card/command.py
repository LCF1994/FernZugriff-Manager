import asynckivy as ak
from kivy.properties import DictProperty, ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.spinner import MDSpinner
from widgets.wrapper.details import ServerDetails


class CommandCard(MDCard):
    image = StringProperty('')
    title = StringProperty('Action')
    btn_icon = StringProperty('centos')
    btn_text = StringProperty('Executar')
    server_target = ObjectProperty(None, allownone=True)
    release_function = DictProperty()

    screen_body = None

    def _snackbar_error(self, message: str) -> None:
        Snackbar(
            text=f'[color=#ee3434]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    def _preper_body(self) -> None:
        body = self.parent.parent.parent.ids.body_container
        self.screen_body = body

        # print(body.children)
        body.ids.container.clear_widgets()

        body.spinner = True

    async def async_cmd(self, long_action, future_reaction) -> None:
        future_reaction(await ak.run_in_thread(long_action))

    def abre_visor_acesso(self, *_) -> None:
        print(
            f'Comando para abrir VisorAcesso no Servidor {self.server_target.host}'
        )

    def get_server_info(self, *_):
        print(
            f'Comando receber informações do Servidor {self.server_target.host}'
        )
        if self.server_target.check_connection():
            self._preper_body()
            ak.start(
                self.async_cmd(
                    self.server_target.get_var, self.reaction_get_server_info
                )
            )
        else:
            self._snackbar_error('No connection to server')

    def reaction_get_server_info(self, data: dict) -> None:
        print(data)
        try:
            self.screen_body.ids.container.add_widget(
                ServerDetails(
                    pos_hint={'center_x': 0.15, 'center_y': 0.525},
                    os=data['CPU'],
                    hostname=data['HOST'],
                    version=data['VERSAO'],
                    database=data['BASE'],
                    gcd=data['GCD'],
                )
            )
        except:
            print('deu ruim')
        try:
            self.screen_body.spinner = False
        except AttributeError:
            self._snackbar_error('Spinner not Found ! - Body not set')

    def executar_remote_command(self, args: dict):
        print(f'Executar comando no Servidor {self.server_target.host}')
        print(args)
