from kivy.properties import BoundedNumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard


class Cover(MDCard):
    message = StringProperty('')
    opacity = BoundedNumericProperty(.5, min=0, max=1, errorvalue=.5)