import asynckivy as ak
from auxiliary.servidor_subprocess import ServidorSAGE
from kivymd.uix.card import MDCard


class PingCard(MDCard):
    def close_card(self, args):
        x, y = args[1].pos

        if not self.collide_point(x, y):
            self.parent.remove_widget(self)

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

        async def server_ping():
            result_value = await ak.run_in_thread(target.check_ping)
            print('ok 3')
            self.ids.spinner.active = False

            print(result_value)
            self.ids.monitor.text_color = (
                success_color if result_value else failure_color
            )

        ak.start(server_ping())


if __name__ == '__main__':
    pass
