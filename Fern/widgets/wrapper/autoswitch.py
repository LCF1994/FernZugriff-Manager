from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import BooleanProperty, StringProperty, ColorProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from widgets.card.help import HelpCard

class AutoSwitch(MDFloatLayout):
    
    def open_popup(self):
        self.parent.add_widget(Popup(
            title='Transferencia Automatica',
            content=MDLabel(
                text='infos',
                ),
            size_hint=(.5,.5), 
            pos_hint={'center_x': .5, 'center_y': .5 },
            auto_dismiss=True,
        ))
    
    def open_popup2(self):
        self.parent.add_widget(
            HelpCard()
        )


class SwitchButton(MDRoundFlatButton):
    text = StringProperty('Button')
    color = ColorProperty([1, 1, 1, 1])
    status = BooleanProperty(False)


    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets['SAGE_1']['AUTOSWITCH'] = self
        self.app.widgets['SAGE_2']['AUTOSWITCH'] = self

        self.text = 'Desligada'
        self.color = self.app.failure_color
        return super().on_kv_post(base_widget)
    

    def toggle(self):
        self.status = not self.status

        if self.status:
            self.text = 'Ligada'
            self.color = self.app.success_color
        else:
            self.text = 'Desligada'
            self.color = self.app.failure_color
    

