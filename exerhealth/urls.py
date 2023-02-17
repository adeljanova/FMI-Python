from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('exerhealth.accounts.urls', )),
    path('clothing-store/', include('exerhealth.clothingstore.urls', namespace='clothes')),
    path('basket/', include('exerhealth.store_basket.urls')),
    path('order/', include('exerhealth.orders.urls')),
    path('forum/', include('exerhealth.forum.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('calorie-tracker/', include('exerhealth.calorie_tracker.urls'))
]
