import re
from collections import defaultdict

from auxiliary.common import CommonCard, CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import (
    ColorProperty,
    ListProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem


class ProcessCard(MDCard, CommonFeatures, CommonCard):
    target = target = ObjectProperty(ServidorSAGE)
    process_list = ListProperty([])

    SAGE_PROCESS_STATUS = defaultdict(lambda: ' ----- ')
    SAGE_PROCESS_STATUS.update(
        {
            0: 'Nao iniciado',
            1: 'Chamado',
            2: 'Esperando',
            3: 'Parado',
            4: 'RODANDO',
            5: 'ERRO',
            6: 'Inibido',
            7: 'Manual',
        }
    )

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['PROCESS_CARD'] = self

        return super().on_kv_post(base_widget)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern = re.compile(r'(?P<Process_Name>^\w+)')

    def close_card(self) -> None:
        Logger.debug('ProcessCard : Card close')
        self.app._on_close_process_card()

        super().close_card()

    def clear_list(self) -> None:
        self.ids.md_list.clear_widgets()

    def create_list(self) -> None:
        # print(f'Data from create_list : {self.process_list}')
        for item in self.process_list:
            new_text = self.pattern.match(item['id']).group('Process_Name')

            self.ids.md_list.add_widget(
                ListItem(
                    text=f'{new_text}',
                    status=f'{self.SAGE_PROCESS_STATUS[item["estad"]]}',
                )
            )

    def update_list(self) -> None:
        self.clear_list()
        self.create_list()

    def _update_process(self, data: list) -> None:
        try:
            self.process_list = data
            self.update_list()
        except TypeError as e:
            print(f'TypeError: {e}')


class ListItem(OneLineAvatarIconListItem):
    status = StringProperty('status')


class ProccessStatus(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True
