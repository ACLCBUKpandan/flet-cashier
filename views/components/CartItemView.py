
from collections.abc import Callable
import flet as ft

from models.CartItem import CartItem
from utils.utils import as_money


class CartItemView (ft.UserControl):
    def __init__(self,
                 item: CartItem,
                 on_click: Callable = lambda: None,
                 on_close: Callable = lambda: None
                 ):
        self.item = item
        self.on_click = on_click
        self.on_close = on_close

    def build(self):
        return ft.ListTile(
            on_click=self.on_click,
            leading=ft.CircleAvatar(
                content=ft.Text(
                    value=f'x {self.item.quantity}'
                )
            ),
            title=ft.Row(controls=[
                ft.Text(
                    value=self.item.product.name
                ),
                ft.VerticalDivider(),
                ft.Text(
                    value=as_money(self.item.subtotal()),
                    weight=ft.FontWeight.W_200
                ),

            ]),
            subtitle=ft.Text(
                value=as_money(self.item.product.price),
                size=12,
                weight=ft.FontWeight.W_200
            ),
            trailing=ft.IconButton(
                icon=ft.icons.CLOSE,
                on_click=self.on_close
            )

        )
