from django.shortcuts import render,redirect
from .models import Cart
from product.models import Product

def cart_home(request):
    cart_obj, new_obj = Cart.objects.get_or_new(request)
    # cart_obj.save()
    context = {'items': cart_obj.products.all()}
    return render(request, 'carts/home.html', context)

def cart_update(request):
    prod_id = 1
    obj = Product.objects.get(id=prod_id)
    cart_obj, new_obj = Cart.objects.get_or_new(request)
    if obj in cart_obj.products.all():
        cart_obj.products.remove(obj)
    else:
        cart_obj.products.add(obj)
    return redirect(to='cart:home')