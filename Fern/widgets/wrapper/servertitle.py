from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


class ServerTitle(MDBoxLayout):
    title = StringProperty('Server XX')
    server_ip = StringProperty('xxx.xxx.xxx.xxx')
