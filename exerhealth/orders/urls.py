from django.urls import path
from .views import place_order,payment_return,payment_cancel

app_name = 'orders'

urlpatterns = [
    path('place-order/', place_order, name='place-order'),
    path('payment-return/', payment_return, name='payment-return'),
    path('payment-cancel/', payment_cancel, name='payment-cancel'),
]
