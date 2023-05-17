from collections.abc import Callable
import flet as ft
from database.db import HOST
from models.Product import Product


class ProductCard (ft.UserControl):
    def __init__(self,
                 product: Product,
                 on_click: Callable = lambda _: None
                 ):
        self.product: Product = product
        self.on_click = on_click

    def build(self):
        return ft.Container(
            on_click=self.on_click,
            border_radius=16,
            content=ft.Column([
                ft.Container(
                    image_src=f'{HOST}/api/files/products/{self.product.id}/{self.product.image}?=thumb100x100',
                    aspect_ratio=16/9,
                    image_fit=ft.ImageFit.COVER
                ),
                ft.Container(
                    padding=ft.padding.only(left=10, right=10),
                    content=ft.Column([
                        ft.Text(
                            self.product.name,
                            weight=ft.FontWeight.W_700,
                            size=18,
                        ),
                        ft.Text(
                            'P {:,.2F}'.format(self.product.price)
                        )

                    ])
                ),

            ]),
            bgcolor=ft.colors.PRIMARY_CONTAINER
        )
