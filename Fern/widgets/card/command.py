from kivymd.uix.card import MDCard
from kivy.properties import StringProperty


class CommandCard(MDCard):
    image = StringProperty('')
    title = StringProperty('Action')
    btn_icon = StringProperty('centos')
    btn_text = StringProperty('Executar')
