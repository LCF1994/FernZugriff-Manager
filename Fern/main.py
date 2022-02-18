import asynckivy as ak
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from servidor import ServidorSAGE

KV = """
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Gerenciador de Acessos'
            elevation: 10
            icon: 'git'
            type: 'top'
        MDFloatLayout:
            PingBox:

<PingBox>:
    size_hint: .6, .9
    pos_hint: {'center_x': .5, 'center_y': .5}
    elevation: '20'
    radius: [dp(36), dp(36), dp(36), dp(36)]
    MDFloatLayout:
        MDIconButton:
            icon: "android"
            theme_text_color: "Custom"
            text_color: [0,1,0,1]
        MDSpinner:
            id: spinner
            size_hint: None, None
            size: dp(20), dp(20)
            pos_hint: {'center_x': .5, 'center_y': .81}
            active: False
        MDIconButton:
            id: monitor
            icon: 'monitor'
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            user_font_size: '75sp'
            pos_hint: {"center_x": .5, "center_y": .8}
        MDLabel:
            halign:'center'
            pos_hint: {'center_x': .5, "center_y": .6}
            text:'SAGE 1'
        MDTextField:
            id: ip_input
            pos_hint: {'center_x': .5, 'center_y': .5}
            size_hint_x: .5
            hint_text: 'IP do servidor'
        MDRaisedButton:
            pos_hint: {'center_x': .5, 'center_y': .3}
            size_hint_x: .5
            text:'Ping !'
            on_release: root.ping(app.sage1, app.success_color, app.failure_color)
"""


class PingBox(MDCard):
    def ping(
        self, target: ServidorSAGE, success_color: list, failure_color: list
    ) -> None:

        server_ip = self.ids.ip_input.text

        if not server_ip:
            self.ids.monitor.text_color = failure_color
            print('vazio')
            return None

        print(f'vou pingar ?! {server_ip}')
        self.ids.spinner.active = True
        target.ip = server_ip
        print(f'target ip = {target.ip}')

        async def server_ping(server_ip):
            result_value = await ak.run_in_thread(target.check_ping)
            print('ok 3')
            self.ids.spinner.active = False

            print(result_value)
            self.ids.monitor.text_color = (
                success_color if result_value else failure_color
            )

        ak.start(server_ping(server_ip))


class FernApp(MDApp):
    sage1 = ServidorSAGE('127.0.0.1')

    def build(self):
        # Config
        self.title = 'Fern'

        # colors
        self.theme_cls.theme_style = 'Dark'

        self.theme_cls.primary_palette = 'Cyan'
        self.theme_cls.primary_hue = '700'

        self.success_color = self.theme_cls.colors['Green']['400']
        self.failure_color = self.theme_cls.colors['Red']['400']

        # Build
        return Builder.load_string(KV)


if __name__ == '__main__':
    FernApp().run()
