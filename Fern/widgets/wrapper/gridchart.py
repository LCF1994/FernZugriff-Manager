from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import NumericProperty


class GridCharts(MDGridLayout):
    cpu = NumericProperty(0)
    memory = NumericProperty(0)
    disk_sage = NumericProperty(0)
    disk_arqs = NumericProperty(0)
    disk_logs = NumericProperty(0)

