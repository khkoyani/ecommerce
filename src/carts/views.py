from django.shortcuts import render,redirect
from .models import Cart
from product.models import Product

def cart_home(request):
    cart_obj, new_obj = Cart.objects.get_or_new(request)
    cart_obj.save()
    return render(request, 'carts/home.html', {})

def cart_update(request):
    product_id = 1
    obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.get_or_new(request)
    cart_obj.products.add(obj)
    return redirect(obj.get_absolute_url())