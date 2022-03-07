from email import message
from operator import index
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

    #cover_conn = BooleanProperty(False)
    #cover_chart = BooleanProperty(False)
#
 #
    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
#
    #    self.CONNECTION_COVER = MainCover(
    #        pos_hint= {'center_x': .5 , 'center_y': .525},
    #        size_hint= (.95, .65),
    #        message='Not Connected',
    #        opacity= .9,
    #    )
#
    #    self.CHARTS_COVER = MainCover(
    #    pos_hint= {'center_x': .66 , 'center_y': .525},
    #    size_hint= (.66, .65),
    #    message= 'GCD Desativado',
    #    opacity= .5,
    #    )

    

        #self.add_widget(self.CHARTS_COVER, index=5)
        

    