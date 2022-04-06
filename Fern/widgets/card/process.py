import re
from collections import defaultdict

from auxiliary.common import CommonCard, CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import (
    BooleanProperty,
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
    spinner = BooleanProperty(True)

    SAGE_PROCESS_STATUS = defaultdict(lambda: ' ------- ')
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
            11: 'Manual',
        }
    )

    RED_STATES = [0, 3, 5, 6]
    GREEN_STATES = [4]

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['PROCESS_CARD'] = self

        return super().on_kv_post(base_widget)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern = re.compile(r'(?P<Process_Name>^\w+)')

    def close_card(self) -> None:
        Logger.debug('ProcessCard : Card close')
        self.app._on_close_process_card(self.target)

        super().close_card()

    def clear_list(self) -> None:
        self.ids.md_list.clear_widgets()

    def create_list(self) -> None:
        self.spinner = False
        # print(f'Data from create_list : {self.process_list}')
        for item in self.process_list:
            new_text = self.pattern.match(item['id']).group('Process_Name')

            if item['estad'] in self.RED_STATES:
                color = self.app.failure_color
            elif item['estad'] in self.GREEN_STATES:
                color = self.app.success_color
            else:
                color = self.app.neutral_color

            self.ids.md_list.add_widget(
                ListItem(
                    text=f'{new_text}',
                    status=f'{self.SAGE_PROCESS_STATUS[item["estad"]]}',
                    color=color,
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
    color = ColorProperty()


class ProccessStatus(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True
