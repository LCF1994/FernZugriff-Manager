from unicodedata import numeric

# from kivymd.app import MDApp
from kivy.properties import (
    BoundedNumericProperty,
    ColorProperty,
    NumericProperty,
    StringProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout


class RoundedChart(MDBoxLayout):
    # app = MDApp.get_running_app()
    name = StringProperty('Title')
    thickness = NumericProperty(20)
    color = ColorProperty([1, 0, 0, 1])
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
