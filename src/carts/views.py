from django.shortcuts import render,redirect
from .models import Cart
from product.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from accounts.models import Guest
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address



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


    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    address_qs = None
    billing_profile, billing_profile_created = BillingProfile.objects.get_or_new(request)

    if billing_profile is not None:
        if request.user.is_authenticated:
            order_obj, order_obj_created = Order.objects.get_or_new(billing_profile, cart_obj)
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    if request.method == 'POST':
        if order_obj.check_done():
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect('cart:done')


    # redirect to success page
    context = {
        'object': order_obj,
        'login_form': login_form,
        'guest_form': guest_form,
        'billing_profile': billing_profile,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
        'address_qs': address_qs,
    }
    return render(request, 'carts/checkout.html', context)

def success(request):
    return render(request, 'carts/success.html', {})