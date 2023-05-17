from database.db import pb
from models.Product import Product


def create_product(name='', price=0):
    pb.collection('products').create(
        {
            'name': name,
            'price': price,
        }
    )


def get_products() -> list[Product]:
    records = pb.collection('products').get_full_list()

    products = map(
        lambda x:
            Product(
                data=x.__dict__['collection_id']
            ), records
    )
    return list(products)
