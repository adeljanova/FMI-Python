from .basket import StoreBasket


def store_basket(request):
    return {'basket': StoreBasket(request)}
