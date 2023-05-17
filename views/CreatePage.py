import flet as ft
from controllers.TransactionController import create_transaction
from models.CartItem import CartItem
from utils.utils import as_money
from views.AppPage import AppPage
from views.components.CartItemView import CartItemView
from views.components.CheckOutDialog import CheckOutDialog
from views.components.ProductCard import ProductCard
from controllers.ProductController import get_products
from models.Product import Product
from views.components.SelectItemDialog import SelectItemDialog
from functools import reduce

from views.components.ReceiptDialog import ReceiptDialog


class CreatePage (AppPage):

    # References of UI elements on screen
    products_grid = ft.Ref[ft.GridView]()
    cart_list = ft.Ref[ft.ListView]()
    total_text = ft.Ref[ft.Text]()

    # Holds the value of total
    total: float = 0

    # Holds the value of all products
    products: list[Product] = []

    # Hold the value of selected items and quantity
    cart: list[CartItem] = []

    def __init__(self, root, route):
        super().__init__(root=root, route=route)

    # Inherits from AppPage
    def did_mount(self):
        """
        After the page is loaded, load the products from the database.
        Then set the products to be loaded to the grid.

        Also sets the cart to list view.
        """
        self.products = get_products()
        self.set_products_to_grid()
        self.set_cart_to_list()

    # Inherits from AppPage
    def get_page(self) -> ft.View:
        """The UI of the page."""
        self.page.appbar = ft.AppBar(
            title=ft.Text('New Transaction '),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_LEFT,
                on_click=lambda _: self.root.go('/dashboard'),
            )
        )
        self.page.controls = [
            ft.ResponsiveRow(
                controls=[
                    ft.Column(controls=[
                        ft.Text('Select Item:',
                                weight=ft.FontWeight.W_700),
                        ft.GridView(
                            ref=self.products_grid,
                            expand=1,
                            runs_count=5,
                            spacing=5,
                            run_spacing=5,
                        )
                    ], col=8),
                    ft.Column([
                        ft.ListView(
                            ref=self.cart_list,
                            auto_scroll=True,
                            expand=1,
                            spacing=10,
                        ),
                        ft.Text('Total:',
                                size=24,
                                weight=ft.FontWeight.W_300),
                        ft.Text('P 0.00',
                                ref=self.total_text,
                                size=36,
                                weight=ft.FontWeight.W_900),
                        ft.FilledButton(
                            'COMPLETE',
                            on_click=self.on_complete_click,
                            width=10000
                        ),

                    ], col=4)
                ], expand=True
            ),
        ]
        return self.page

    def set_cart_to_list(self,):
        """
        Adapter of list[CartItem] to ListView item
        """
        self.cart_list.current.controls.clear()

        if len(self.cart) <= 0:
            self.cart_list.current.controls.append(
                ft.Text("No items added."),
            )
            self.page.update()
            return
        cart = map(
            lambda x:
                CartItemView(
                    item=x,
                    on_click=lambda _: self.on_cart_item_click(x),
                    on_close=lambda _: self.remove_cart_item(x),
                ), self.cart)

        for i in list(cart):
            self.cart_list.current.controls.append(i.build())

        self.page.update()

    def on_cart_item_click(self, item: CartItem):
        """
        Handles when the user clicks an item on the cart.

        Shows dialog when the user clicks at cart item.

        item: CartItem
        The item that is selected
        """

        # Show dialog if there is no item in the cart
        dialog = SelectItemDialog(
            on_finish=self.on_cart_item_finish,
            item=item.product,
            root=self.root,
            quantity=item.quantity,
        )
        dialog.build()
        dialog.show()

    def on_cart_item_finish(self, item: Product, quantity: int):
        """
        Handles when the user has finished editing the quantity
        of the selected cart item.

        Edits the quantity of the selected cart item.

        item: Product
        The product that is selected.

        quantity: int
        The quantity of the selected product.
        """

        # Search cart and set the quantity of the item
        for i in self.cart:

            if i.product == item:
                i.quantity = quantity

        self.set_cart_to_list()
        self.set_total()

    def remove_cart_item(self, item: CartItem):
        """
        Remove item from the cart

        item: CartItem
        The selected item of the cart
        """
        self.cart.remove(item)
        self.set_cart_to_list()
        self.set_total()

    def set_products_to_grid(self):
        """
        Sets the 'products' to grid.
        """

        # Clear the grid first
        self.products_grid.current.controls.clear()

        # Set each products to ProductCard component
        # See views.components.ProductCard
        product_map = map(lambda x: ProductCard(
            product=x,
            on_click=lambda _: self.on_product_selected(x)
        ), self.products)

        # Set product component to grid
        for i in list(product_map):
            self.products_grid.current.controls.append(i.build())
        self.page.update()

    def on_complete_click(self, _):
        """
        Handles when 'Complete' button is cliked.

        Displays bottom sheet bar when complete button is clicked.
        If there is no item in the cart then shows a snack bar.
        """

        if len(self.cart) <= 0:

            snack = ft.SnackBar(
                content=ft.Text('Cart is Empty'),
            )
            self.root.snack_bar = snack
            self.root.snack_bar.open = True
            self.root.update()
            return

        checkout = CheckOutDialog(
            root=self.root,
            on_finish=self.on_transaction_finish,
            total=self.total,
        )

        self.root.overlay.append(checkout.build())
        self.root.update()

    def on_transaction_finish(self,
                              cash: float,
                              change: float,
                              sheet: CheckOutDialog):
        """
        Saves the transaction to the database.
        Displays ReceiptDialog after.

        cash: float
        The cash from the bottom sheet view

        change: float
        The change based on the total and the cash


        sheet: CheckOutDialog
        Reference to the BottomSheet
        """
        transaction = create_transaction(
            cart=self.cart, cash=cash, change=change)
        self.cart.clear()
        self.set_cart_to_list()
        sheet.close()

        dialog = ReceiptDialog(
            transaction=transaction,
            root=self.root,
            on_ok=self.on_new_transaction,
            on_history=self.on_history_click,
        )
        dialog.build()
        dialog.show()

    def on_new_transaction(self):
        """
        Runs when the user clicks 'OK' when a transaction is finished.
        """

    def on_history_click(self):
        """
        Runs when the user clicks 'HISTORY', go to history page
        """
        pass

        self.root.go('/history')

    def on_product_selected(self, item: Product):
        """
        Handles when a user clicks a product in the grid.

        Check if the selected item is already in the cart.
        If so, show a snackbar. Otherwise show dialog to
        edit quantity.

        item: Product
        The selected product of the grid.
        """
        # Check if current item is in the cart
        cart_count = list(
            filter(
                lambda x: x.product == item, self.cart)
        )
        # If there is already one, show a snackbar and exit
        if len(cart_count) >= 1:
            self.root.snack_bar = ft.SnackBar(
                ft.Text('Item already in the cart.')
            )
            self.root.snack_bar.open = True
            self.root.update()
            return

        # Show dialog if there is no item in the cart
        dialog = SelectItemDialog(
            on_finish=self.on_item_picked,
            item=item,
            root=self.root
        )
        dialog.build()
        dialog.show()

    def on_item_picked(self, item: Product, qty: int):
        """
        Handles when the user has picked and set the quantity of the selected
        product.

        Add the picked item to the 'cart' list.

        item: Product
        The selected item.

        qty: int
        The selected quantity
        """
        self.cart.append(
            CartItem(
                product=item,
                quantity=qty,
            )
        )
        self.set_cart_to_list()
        self.set_total()

    def set_total(self):
        """
        Set the total UI control.
        """
        self.calculate_total()
        self.total_text.current.value = as_money(self.total)
        self.total_text.current.update()

    def calculate_total(self):
        """
        Sets the the 'total' variable to the total of cart items
        """
        self.total = reduce(lambda a, b: a+b.subtotal(), self.cart, 0)
