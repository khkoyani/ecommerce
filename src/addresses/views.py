from django.shortcuts import render, redirect
from .forms import AddressForm
from .models import Address
from django.utils.http import is_safe_url
from billing.models import BillingProfile
from .models import Address

def address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {'form': form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, billing_profile_new = BillingProfile.objects.get_or_new(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            address_type = request.POST.get('address_type', 'shipping')
            instance.address_type = address_type
            instance.save()
            request.session[address_type + "_address_id"] = instance.id

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('cart:checkout')
        else:
            # space for error mesage
            return redirect('cart:checkout')
    return redirect('cart:checkout')

def use_saved_address_view(request):
    print('1')
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post
        if request.method =='POST':
            print(request.POST)
            billing_profile, billing_profile_new = BillingProfile.objects.get_or_new(request)
            if billing_profile is not None:
                id = request.POST.get('shipping_address')
                address_type = request.POST.get('address_type')
                address = Address.objects.filter(id=id).first()

                request.session[address_type + "_address_id"] = address.id

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
    return redirect('cart:checkout')