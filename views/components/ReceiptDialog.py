from collections.abc import Callable
import flet as ft
from flet_core import DataRow

from models.Transaction import Transaction
from views.components.CartItemView import as_money


class ReceiptDialog  (ft.UserControl):

    dialog = ft.Ref[ft.AlertDialog]()

    def __init__(self,
                 transaction: Transaction,
                 root: ft.Page,
                 on_ok: Callable,
                 on_history: Callable
                 ):
        self.transaction: Transaction = transaction
        self.root = root
        self.on_ok = on_ok
        self.on_history = on_history

    def set_rows(self) -> list[DataRow]:
        rows = map(lambda x:
                   ft.DataRow(cells=[
                       ft.DataCell(ft.Text(x.product.name)),
                       ft.DataCell(ft.Text(as_money(x.product.price))),
                       ft.DataCell(ft.Text(f'x {x.quantity}')),
                       ft.DataCell(ft.Text(as_money(x.subtotal())))
                   ]),
                   self.transaction.cart_items)
        return list(rows)

    def show(self):
        self.root.dialog = self.dialog.current
        self.dialog.current.open = True
        self.root.update()

    def hide(self):
        self.dialog.current.open = False
        self.root.update()

    def build(self):
        return ft.AlertDialog(
            ref=self.dialog,
            content=ft.Column(controls=[
                ft.Text('Transaction Complete!',
                        weight=ft.FontWeight.W_700
                        ),
                ft.Text('Total: ',),
                ft.Text(as_money(self.transaction.calculate_total()),
                        size=32, weight=ft.FontWeight.W_700
                        ),
                ft.Text('Cash: ',),
                ft.Text(as_money(self.transaction.cash),
                        size=24, weight=ft.FontWeight.W_400
                        ),
                ft.Text('Change: ',),
                ft.Text(as_money(self.transaction.change),
                        size=24, weight=ft.FontWeight.W_400
                        ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Name")),
                        ft.DataColumn(ft.Text("Price")),
                        ft.DataColumn(ft.Text("Quantity")),
                        ft.DataColumn(ft.Text("Subtotal")),
                    ],
                    rows=self.set_rows()),
            ]),
            actions=[
                ft.TextButton('OK', on_click=lambda _: self.on_ok()),
                ft.TextButton('HISTORY', on_click=lambda _: self.on_history()),
            ]
        )
