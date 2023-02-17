from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


@login_required(login_url='login')
def product_all(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'clothes/clothes_store.html', context)


@login_required(login_url='login')
def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'clothes/clothing_category.html', context)


@login_required(login_url='login')
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {'product': product}
    return render(request, 'clothes/single_product.html', context)
