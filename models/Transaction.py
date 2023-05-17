

from pocketbase.models.record import BaseModel
from controllers.ProductController import Product

from controllers.TransactionController import CartItem
from functools import reduce


class Transaction(BaseModel):
    cart_items: list[CartItem]
    cash: float
    change: float

    def load(self, data: dict):
        super().load(data=data)
        self.cash = float(data.get('cash', 0))
        self.change = float(data.get('change', 0))

        cart = data.get('expand', {}).get('details', [])

        products: list[CartItem] = []
        for i in cart:
            quantity = i.get('quantity', 0)
            print(i['expand']['product'])
            product = Product().load(data=i['expand']['product'])
            products.append(CartItem(product=product, quantity=quantity))

        self.cart_items = products
        return self

    def calculate_total(self):
        return reduce(lambda a, b: a+b.subtotal(), self.cart_items, 0)
