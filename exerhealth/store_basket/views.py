from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from exerhealth.clothingstore.models import Product
from .basket import StoreBasket


@login_required(login_url=login)
def basket_summary(request):
    basket = StoreBasket(request)
    context = {'basket': basket}
    return render(request, 'basket/store_basket.html', context)


@login_required(login_url=login)
def basket_add(request):
    basket = StoreBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response


@login_required(login_url=login)
def basket_update(request):
    basket = StoreBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response


@login_required(login_url=login)
def basket_delete(request):
    basket = StoreBasket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response

