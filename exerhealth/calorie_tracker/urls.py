from django.urls import path
from . import views

app_name = 'calorie_tracker'

urlpatterns = [
    path('show-food-lists/', views.show_food_lists, name='show_food_lists'),
    path('show-food-items/', views.show_food_items, name='show_food_items'),
    path('food_item_detail/', views.food_item_detail, name='food_item_detail'),
]