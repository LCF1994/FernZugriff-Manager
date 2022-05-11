from kivymd.uix.card import MDCard
from auxiliary.common import CommonCard
from kivy.properties import StringProperty


class HelpCard(MDCard, CommonCard):
    title = StringProperty('Title')
    content = StringProperty('Description')