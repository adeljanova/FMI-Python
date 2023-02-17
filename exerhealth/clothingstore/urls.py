from django.urls import path
from exerhealth.clothingstore import views

app_name = 'clothingstore'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('<slug:category_slug>', views.category_list, name='category_list'),
]
