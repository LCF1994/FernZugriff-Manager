from auxiliary.common import CommonCard
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


class HelpCard(MDCard, CommonCard):
    title = StringProperty('Title')
    content = StringProperty('Description')
