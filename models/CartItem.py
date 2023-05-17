from dataclasses import dataclass
from models.Product import Product


@dataclass
class CartItem:
    product: Product
    quantity: int

    def subtotal(self) -> float:
        return self.product.price * float(self.quantity)
