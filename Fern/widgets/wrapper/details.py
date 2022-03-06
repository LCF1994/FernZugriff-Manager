from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from auxiliary.servidor_paramiko import ServidorSAGE


class ServerDetails(MDBoxLayout):
    os = StringProperty('linux')
    hostname = StringProperty('Host')
    version = StringProperty('xx-xx')
    database = StringProperty('undefined')
    gcd = StringProperty('desativado')
      

    def update_data(self, srv):
        if type(srv) is ServidorSAGE:
            self.os = srv.var['CPU']
            self.hostname = srv.var['HOST']
            self.version = srv.var['VERSAO']
            self.database = srv.var['BASE']
        