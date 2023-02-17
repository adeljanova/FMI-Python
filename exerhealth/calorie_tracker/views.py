from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import FoodList, FoodItem


@login_required(login_url='login')
def show_food_lists(request):
    food_lists = FoodList.objects.all()
    context = {'food_lists': food_lists}
    return render(request, 'calorie_tracker/show_food_list.html', context)


@login_required(login_url='login')
def show_food_items(request, category_slug=None):
    food_list = get_object_or_404(FoodList, slug=category_slug)
    food_item = FoodItem.objects.filter(type_item=food_list)
    context = {'food_list': food_list, 'food_item': food_item}
    return render(request, 'calorie_tracker/show_food_item.html', context)


@login_required(login_url='login')
def food_item_detail(request):
    food_item = get_object_or_404(FoodItem)
    context = {'food_item': food_item}
    return render(request, 'calorie_tracker/food_item_detail.html', context)
