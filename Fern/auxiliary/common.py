import asynckivy as ak
from kivymd.uix.snackbar import Snackbar


class CommonFeatures:
    def _snackbar_info(self, message: str) -> None:
        Snackbar(
            text=f'{message}',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    def _snackbar_warn(self, message: str) -> None:
        Snackbar(
            text=f'[color=#eeee00]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    def _snackbar_error(self, message: str) -> None:
        Snackbar(
            text=f'[color=#ee3434]{message}[/color]',
            snackbar_x='10dp',
            snackbar_y='10dp',
            size_hint_x=0.95,
        ).open()

    # async def async_cmd(self, async_action, future_reaction) -> None:
    #    future_reaction(await ak.run_in_thread(async_action))


class CommonCard:
    def close_card(self) -> None:
        self.parent.remove_widget(self)

    def check_card_focus(self, args) -> None:
        x, y = args[1].pos

        # check unfocus
        if not self.collide_point(x, y):
            self.close_card()
