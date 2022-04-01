from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.logger import Logger
from kivy.properties import NumericProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout


class GridCharts(MDGridLayout):
    cpu = NumericProperty(0)
    memory = NumericProperty(0)
    disk_sage = NumericProperty(0)
    disk_arqs = NumericProperty(0)
    disk_logs = NumericProperty(0)

    target = ObjectProperty(ServidorSAGE)

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['GRID_CHARTS'] = self

        return super().on_kv_post(base_widget)

    def update_charts_info(self, data_received: dict) -> None:
        try:
            self.cpu = data_received['cpu']
            self.memory = data_received['memory']
            self.disk_sage = data_received['disk_sage']
            self.disk_arqs = data_received['disk_arqs']
            self.disk_logs = data_received['disk_logs']
        except KeyError:
            Logger.error('Charts : Key not found in data received')
