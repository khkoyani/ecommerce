from django.shortcuts import render,redirect
from .models import Cart
from product.models import Product
from orders.models import Order



def cart_home(request):

    cart_obj, new_obj = Cart.objects.get_or_new(request)
    # cart_obj.save()
    context = {'cart': cart_obj}
    return render(request, 'carts/home.html', context)

def cart_update(request):
    prod_id = request.POST.get('product_id')
    if prod_id is not None:
        obj = Product.objects.get(id=prod_id)
        cart_obj, new_obj = Cart.objects.get_or_new(request)
        if obj in cart_obj.products.all():
            cart_obj.products.remove(obj)
        else:
            cart_obj.products.add(obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect(to='cart:home')

def checkout(request):
    cart_obj, new_obj = Cart.objects.get_or_new(request)
    order_obj = None
    if new_obj or cart_obj.products.count() ==0:
        return redirect('cart:home')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    context = {
        'object': order_obj
    }
    return render(request, 'carts/checkout.html', context)