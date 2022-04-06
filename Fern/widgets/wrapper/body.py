from auxiliary.servidor_paramiko import ServidorSAGE
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from widgets.cover.cover import Cover
from widgets.wrapper.chart import RoundedChart
from widgets.wrapper.details import ServerDetails
from widgets.wrapper.gridchart import GridCharts


class BodyContainer(MDFloatLayout):
    target = ObjectProperty(ServidorSAGE)
    spinner = BooleanProperty(False)
    spinner_palette = ListProperty(
        [
            [0.286, 0.843, 0.596, 1],
            [0.356, 0.321, 0.866, 1],
            [0.886, 0.3647, 0.592, 1],
            [0.878, 0.905, 0.407, 1],
        ]
    )

    def on_kv_post(self, base_widget):
        self.app = MDApp.get_running_app()
        self.app.widgets[self.target.name]['SCREEN_BODY'] = self

        return super().on_kv_post(base_widget)

    def update_connection(self, connected: bool) -> None:
        if connected is True:
            self._hide_cover(self.ids.cover_all)
        else:
            self._show_cover(
                self.ids.cover_all,
                cover_message=f'DESCONECTADO',
                darkness=0.925,
            )

    def update_gcd_state(self, gcd_running: bool) -> None:
        if gcd_running is True:
            self._hide_cover(self.ids.cover_all)
            self._hide_cover(self.ids.cover_charts)
        else:
            self._show_cover(
                self.ids.cover_charts,
                cover_message='GCD DESATIVADO',
                darkness=0.75,
            )

    def _hide_cover(self, cover: Cover) -> None:
        cover.message = ''
        cover.opacity = 0

    def _show_cover(
        self, cover: Cover, cover_message: str, darkness: 0.5
    ) -> None:
        cover.message = cover_message
        cover.opacity = darkness
