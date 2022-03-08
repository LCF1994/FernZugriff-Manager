from kivy.properties import (
    BoundedNumericProperty,
    ColorProperty,
    NumericProperty,
    StringProperty,
)
from kivymd.uix.boxlayout import MDBoxLayout


class RoundedChart(MDBoxLayout):
    name = StringProperty('Title')
    thickness = NumericProperty(20)
    color = ColorProperty([1, 0, 0, 1])
    value = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
