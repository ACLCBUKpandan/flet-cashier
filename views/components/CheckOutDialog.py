from collections.abc import Callable
import re
import flet as ft

from views.CreatePage import as_money


class CheckOutDialog (ft.UserControl):

    cash = ft.Ref[ft.TextField]()
    sheet = ft.Ref[ft.BottomSheet]()
    button = ft.Ref[ft.FilledButton]()
    change_text = ft.Ref[ft.Text]()

    change: float = 0

    def __init__(self,
                 root: ft.Page,
                 on_finish: Callable,
                 total: float = 0
                 ):
        self.root = root
        self.on_finish = on_finish
        self.total = total

    def calculate_change(self,):
        cash = 0 if self.cash.current.value is None else float(
            self.cash.current.value)
        self.change = float(cash) - self.total

    def on_cash_change(self, _):
        text = self.cash.current.value
        text = "" if text is None else text
        pattern = r'^\d+$'
        if not re.match(pattern, text):
            text = text[:-1]
            self.cash.current.value = text
        if text == "0":
            self.cash.current.value = "1"

        self.calculate_change()
        self.change_text.current.value = as_money(self.change)

        if self.change < 0:
            self.button.current.disabled = True
            self.cash.current.error_text = "Insufficient Funds."

        else:
            self.button.current.disabled = False
            self.cash.current.error_text = ""

        self.change_text.current.update()
        self.cash.current.update()
        self.button.current.update()

    def on_close(self, _):
        """Closes the sheet."""
        self.sheet.current.open = False
        self.sheet.current.update()

    def close(self,):
        """Closes the sheet."""
        self.sheet.current.open = False
        self.sheet.current.update()

    def build(self,) -> ft.BottomSheet:
        return ft.BottomSheet(
            ref=self.sheet,
            open=True,
            content=ft.Container(
                width=500,
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text('Complete Transaction: '),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE,
                                    on_click=self.on_close,
                                )
                            ]
                        ),
                        ft.TextField(
                            ref=self.cash,
                            label="Cash",
                            prefix=ft.Text('P '),
                            on_change=self.on_cash_change
                        ),
                        ft.Text('Total: ', size=24,
                                weight=ft.FontWeight.W_100,),
                        ft.Text(
                            value=as_money(self.total),
                            size=32, weight=ft.FontWeight.W_900),
                        ft.Text('Change: ', size=24,
                                weight=ft.FontWeight.W_100,),
                        ft.Text(
                            ref=self.change_text,
                            value=as_money(self.change),
                            size=32, weight=ft.FontWeight.W_900),
                        ft.FilledButton(
                            ref=self.button,
                            disabled=True,
                            on_click=lambda _: self.on_finish(
                                float(
                                    0 if self.cash.current.value is None
                                    else self.cash.current.value),
                                self.change,
                                self
                            ),
                            width=100000,
                            text="COMPLETE"
                        ),

                    ]
                )
            ),
        )
