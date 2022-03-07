from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from auxiliary.servidor_paramiko import ServidorSAGE
import asynckivy as ak

class ServerDetails(MDBoxLayout):
    os = StringProperty('linux')
    hostname = StringProperty('Host')
    version = StringProperty('xx-xx')
    database = StringProperty('undefined')
    gcd = StringProperty('desativado')
      

    def update_data(self, srv):
        ak.start(self._request_data(srv))

    async def _request_data(self, srv) -> None:
        data = await ak.run_in_thread(srv.get_var)
        self._update_widget_data(data)
        
    def _update_widget_data(self, data:dict) -> None:
        self.os = data['CPU']
        self.hostname = data['HOST']
        self.version = data['VERSAO']
        self.database = data['BASE']
        self.gcd = data['GCD']
        