
from typing import Optional
import flet as ft
from controllers.TransactionController import get_transactions
from models.Transaction import Transaction
from views.AppPage import AppPage
from views.components.CartItemView import as_money


class HistoryPage (AppPage):

    transaction_list = ft.Ref[ft.ListView]()
    cart_item = ft.Ref[ft.DataTable]()

    list_items: list[ft.ListTile] = []

    def __init__(self, root, route):
        super().__init__(root=root, route=route)

    transactions: list[Transaction] = []
    selected_transaction: Optional[Transaction] = None

    def did_mount(self):
        self.load_transactions_to_listview()

    def on_transaction_click(self, transaction: Transaction):
        items = transaction.cart_items

        rows = map(lambda x: ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(x.product.name)),
                ft.DataCell(ft.Text(as_money(x.product.price))),
                ft.DataCell(ft.Text(as_money(x.quantity))),
                ft.DataCell(ft.Text(as_money(x.subtotal()))),
            ]
        ), items)
        columns = [
            ft.DataColumn(ft.Text("Product")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Subtotal")),
        ]
        dialog = ft.AlertDialog(
            title=ft.Text(
                f'{transaction.created}       |         ' +
                f'{as_money(transaction.calculate_total())}'),
            content=ft.DataTable(
                columns=columns,
                rows=list(rows)
            )
        )

        self.root.dialog = dialog
        dialog.open = True

        self.root.update()

    def load_transactions_to_listview(self):
        """
        Gets transaction and loads it to the list view
        """
        # clear transaction list
        self.list_items.clear()

        # Get the last transaction with the recent first.
        self.transactions = get_transactions()[::-1]

        self.selected_transaction = self.transactions[0]

        items = map(
            lambda x:
                ft.ListTile(
                    leading=ft.Text(f"{x.created}"),
                    title=ft.Text(
                        f"Total : {as_money(x.calculate_total())}  "),
                    on_click=lambda _: self.on_transaction_click(x)

                ), self.transactions)
        # Set list items

        self.transaction_list.current.controls = list(items)
        self.transaction_list.current.update()

    def get_page(self) -> ft.View:
        self.page.appbar = ft.AppBar(
            title=ft.Text('History'),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_LEFT,
                on_click=lambda _: self.root.go('/dashboard'),
            )
        )
        self.page.controls = [
            ft.ResponsiveRow(
                controls=[
                    ft.ListView(
                        ref=self.transaction_list
                    ),
                    ft.DataTable(
                        ref=self.cart_item
                    ),
                ]
            )
        ]
        return self.page
