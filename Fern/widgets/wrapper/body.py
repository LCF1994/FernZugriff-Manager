from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from widgets.wrapper.details import ServerDetails
from auxiliary.servidor_paramiko import ServidorSAGE
from widgets.wrapper.chart import RoundedChart
from widgets.cover.cover import MainCover


class BodyContainer(MDFloatLayout):
    target = ObjectProperty(None)
    spinner = BooleanProperty(False)
    spinner_palette = ListProperty(
        [
            [0.286, 0.843, 0.596, 1],
            [0.356, 0.321, 0.866, 1],
            [0.886, 0.3647, 0.592, 1],
            [0.878, 0.905, 0.407, 1],
        ]
    )
