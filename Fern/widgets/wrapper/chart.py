from unicodedata import numeric
from kivymd.uix.boxlayout import MDBoxLayout
#from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty, ColorProperty


class RoundedChart(MDBoxLayout):
    #app = MDApp.get_running_app()
    name = StringProperty('Title')
    thickness = NumericProperty(20)
    color = ColorProperty([1,0,0,1])
    value = NumericProperty(0)