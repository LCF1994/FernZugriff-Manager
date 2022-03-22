from collections import defaultdict
from random import random as rd

import asynckivy as ak
from auxiliary.common import CommonCard, CommonFeatures
from kivy.clock import Clock
from kivy.properties import (
    ColorProperty,
    ListProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

#
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem


class ProccessCard(MDCard, CommonFeatures, CommonCard):
    app = ObjectProperty(None)
    server_target = server_target = ObjectProperty(None)
    proccess_list = ListProperty([])

    SAGE_PROCCESS_STATUS = defaultdict(lambda: ' ----- ')
    SAGE_PROCCESS_STATUS.update(
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_list()

    def on_enter(self):
        print('On-enter')
        self.app.RUNNING_CLOCK['proccess'] = Clock.schedule_interval(
            self.update_proccess_list, 30
        )
        return super().on_enter()

    def close_card(self) -> None:

        try:
            self.app.RUNNING_CLOCK['proccess'].cancel()
        except (KeyError, TypeError):
            print('Proccess not Scheduled')
        return super().close_card()

    def clear_list(self) -> None:
        self.ids.md_list.clear_widgets()

    def create_list(self) -> None:
        # item_list = [x for x in range(1, 10 + 1)]
        # self.proccess_list =[{'id': 'ValidaCtg-srv1', 'estad': 0}, {'id': 'SAR_anacon-srv1', 'estad': 0},]

        for item in self.proccess_list:
            self.ids.md_list.add_widget(
                ListItem(
                    text=f'{item["id"]}',
                    status=f'{self.SAGE_PROCCESS_STATUS[item["estad"]]}',
                )
            )

    def update_list(self) -> None:
        self.clear_list()
        self.create_list()

    def update_proccess_list(self, *args) -> None:
        print('Updating list of proccess: Getting data')
        ak.start(
            self.async_cmd(
                self.server_target.get_server_proccess, self._update_self_list
            )
        )

    def _update_self_list(self, data: list) -> None:
        print('Updating list of proccess: done')
        try:
            self.proccess_list = data
            self.update_list()
        except TypeError as e:
            print(f'TypeError: {e}')


class ListItem(OneLineAvatarIconListItem):
    status = StringProperty('status')


class ProccessStatus(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True
