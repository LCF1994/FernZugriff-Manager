import asynckivy as ak
from kivy.properties import ColorProperty, OptionProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class ServerDetails(MDBoxLayout):
    os = StringProperty('linux')
    hostname = StringProperty('Host')
    version = StringProperty('xx-xx')
    database = StringProperty('undefined')
    dbtype = StringProperty('undefined')
    gcd = StringProperty('desativado')
    gcd_color = ColorProperty([1, 0, 0, 1])
    sound = StringProperty('undefined')
    redundancy = StringProperty('undefined')
    network_node = StringProperty('undefined')

    def update_data(self, srv):
        ak.start(self._request_data(srv))

    async def _request_data(self, srv) -> None:
        data = await ak.run_in_thread(srv.get_var)
        self._update_widget_data(data)

    def _update_widget_data(self, data: dict) -> None:
        self.os = data['CPU']
        self.hostname = data['HOST']
        self.version = data['VERSAO']
        self.database = data['BASE']
        self.gcd = data['GCD']
        self.gcd_color = data['GCD_COR']
        self.dbtype = data['MODELO']
        self.sound = data['SOM']
        self.redundancy = data['DIFUSAO']
        self.network_node = data['LOCAL']


class Item(MDBoxLayout):
    title = StringProperty('ITEM')
    value = StringProperty('undefined')
    theme = OptionProperty(
        'Custom',
        options=[
            'Primary',
            'Secondary',
            'Hint',
            'Error',
            'Custom',
            'ContrastParentBackground',
        ],
        allownone=True,
    )
    color = ColorProperty([1, 1, 1, 1])
