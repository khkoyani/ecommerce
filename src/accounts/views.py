from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import Guest

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password)
    return render(request, 'accounts/register.html', context)



def login_page(request):
    form=LoginForm(request.POST or None)
    context = {'form':form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
        else:
            print('adsf')
    return render(request, 'accounts/login.html', context)

def guest_login_view(request):
    form=GuestForm(request.POST or None)
    context = {'form':form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if form.is_valid():
        email=form.cleaned_data.get('email')
        guest=Guest.objects.create(email=email)
        request.session['guest_id'] = guest.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('home')
    return render(request, 'accounts/register.html', context)


