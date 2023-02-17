import json
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from .models import Order, OrderItem
from django.conf import settings
import uuid


@login_required(login_url=login)
def payment_return(request):
    messages.success(request, "You\'ve successfully made an order!")
    return render(request, 'payment_success.html')


@login_required(login_url=login)
def payment_cancel(request):
    messages.error(request, "Your order nas been cancelled!")
    return render(request, 'payment_failure.html')


@login_required(login_url=login)
def place_order(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': Order.total_paid,
        'item_name': OrderItem.order,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'BGN',
        'notify_url': f'http//{host}{reverse("paypal-ipn")}',
        'return_url': f'http//{host}{reverse("orders:payment-return")}',
        'cancel_return': f'http//{host}{reverse("orders:payment-cancel")}',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form}
    return render(request, 'order/place_order.html', context)
