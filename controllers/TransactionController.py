

from controllers.AuthController import pb
from views.components.CartItemView import CartItem
from models.Transaction import Transaction


def create_transaction(cart: list[CartItem],
                       cash: float = 0,
                       change: float = 0) -> Transaction:

    item = []
    for i in cart:
        create = pb.collection('cart').create(
            {
                'product': i.product.id,
                'quantity': i.quantity
            }).__dict__['collection_id']

        item.append(create['id'])

    user = "" if pb.auth_store.model is None else pb.auth_store.model.id

    transaction = pb.collection('transaction').create(
        {
            'details': item,
            'user': user,
            'cash': cash,
            'change': change
        },
        {
            'expand': 'details.product'
        }
    )
    return Transaction().load(data=transaction.__dict__['collection_id'])


def get_transactions() -> list[Transaction]:

    data = pb.collection('transaction').get_full_list(
        # Include the product information, not just the id
        query_params={'expand': 'details.product'}
    )
    transactions = map(
        lambda x:
            Transaction().load(data=x.__dict__['collection_id']), data
    )

    return list(transactions)
