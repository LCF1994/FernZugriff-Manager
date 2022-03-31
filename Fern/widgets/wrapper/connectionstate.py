import asynckivy as ak
from auxiliary.common import CommonFeatures
from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class ConnectionState(MDBoxLayout, CommonFeatures):
    conn_state = StringProperty('Offline')
    target = ObjectProperty(None)
    spinner = BooleanProperty(False)

    app = None
    screen_body = None
    clock_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clock_list.extend(
            [
                self._update_gcd_state,
                self._update_charts_value,
            ]
        )

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['CONN_STATE'] = self

        self.screen_body = self.parent.parent.ids.body_container

        return super().on_kv_post(base_widget)

    def connect(self) -> None:
        if self.target.host == 'xxx.xxx.xxx.xxx':
            self._snackbar_error('Configure um IP valido')

        else:
            self.spinner = True
            self.app.connect_to_server(self.target)

    def update_connection(self, data: bool) -> None:
        self.spinner = False
        print(f'Dados recebidos: {data}')

        if data is True:
            self.positive_conn()
        else:
            self.negative_conn()

    def positive_conn(self):
        self.conn_state = 'Online'
        # Must be implemented
        # change connection btn to disconnection btn

    def negative_conn(self):
        self.conn_state = 'Offline'
        # Must be implemented
        # change disconnection btn to connection btn

        self._snackbar_error('Falha na Conexao')

    # functions for update charts - clock event
    def _update_charts_value(self, *args) -> None:
        if self.target.gcd:
            print('Requesting Charts Update ...')
            ak.start(
                self.async_cmd(
                    self.target.get_performance,
                    self._update_charts_value_with_data_received,
                )
            )
        else:
            print('GCD not running')

    def _update_charts_value_with_data_received(
        self, data_received: dict
    ) -> None:
        print(f'Requesting Charts Update: {data_received} - Done')

        self.screen_body.ids.grid_chart.cpu = data_received['cpu']
        self.screen_body.ids.grid_chart.memory = data_received['memory']
        self.screen_body.ids.grid_chart.disk_sage = data_received['disk_sage']
        self.screen_body.ids.grid_chart.disk_arqs = data_received['disk_arqs']
        self.screen_body.ids.grid_chart.disk_logs = data_received['disk_logs']
