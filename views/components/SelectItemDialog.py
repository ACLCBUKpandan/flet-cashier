from collections.abc import Callable
import flet as ft

import re
from models.Product import Product
from views.components.ProductCard import HOST


class SelectItemDialog (ft.UserControl):

    qty = ft.Ref[ft.TextField]()
    alert = ft.Ref[ft.AlertDialog]()

    def __init__(self,
                 on_finish: Callable,
                 item: Product,
                 root: ft.Page,
                 quantity: int = 1
                 ):
        self.on_finish = on_finish
        self.item = item
        self.root = root
        self.quantity = quantity

    def on_qty_change(self, _):
        """Handles qty change.
        Set qty only take number.
        """
        text = self.qty.current.value
        text = "" if text is None else text
        pattern = r'^\d+$'
        if not re.match(pattern, text):
            text = text[:-1]
            self.qty.current.value = text
        if text == "0":
            self.qty.current.value = "1"
        self.qty.current.update()

    def build(self,):
        return ft.AlertDialog(
            ref=self.alert,
            title=ft.Column(
                controls=[
                    ft.Text(
                        value=self.item.name,
                        weight=ft.FontWeight.W_600,
                        size=32
                    ),
                    ft.Text(
                        'P {:,.2f}'.format(self.item.price),
                        size=16
                    ),

                ]
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        image_src=f'{HOST}/api/files/products/{self.item.id}/{self.item.image}?=thumb200x200',
                        height=400,
                        width=400,
                        image_fit=ft.ImageFit.COVER,
                    ),
                    ft.TextField(
                        ref=self.qty,
                        label="Quantitiy",
                        keyboard_type=ft.KeyboardType.NUMBER,
                        max_length=2,
                        min_lines=1,
                        value=str(self.quantity),
                        on_change=self.on_qty_change,
                    )
                ]),
            actions=[
                ft.TextButton('CANCEL', on_click=self.on_cancel),
                ft.TextButton('OK', on_click=self.on_ok),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def show(self):
        """Shows the dialog"""
        self.alert.current.open = True
        self.root.dialog = self.alert.current
        self.root.update()

    def on_ok(self, _):
        """When the user clicks ok.
        If quantity is empty then show error on screen,
        else call on_finish function and closes the dialog"""
        if self.qty.current.value == "":
            self.qty.current.error_text = "Cannot be empty"
            self.root.update()
            self.update()
            return

        self.on_finish(self.item, self.qty.current.value)
        self.alert.current.open = False
        self.root.update()

    def on_cancel(self, _):
        """Closes when user clicks Cancel"""
        self.alert.current.open = False
        self.root.update()
