from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton


class ConnectionState(MDBoxLayout):
    def connect(self, target):
        self.remove_widget(self.ids.conn_btn)
        self.add_widget(RefreshButton())


class RefreshButton(MDIconButton):
    def refresh(self):
        current_text = self.parent.ids.text.text

        if current_text == 'Offline':
            self.parent.ids.text.text = 'Online'
        else:
            self.parent.ids.text.text = 'Offline'
