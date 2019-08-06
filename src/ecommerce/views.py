from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

def about(request):
    context = {'title': 'about', 'body':'About us'}
    return render(request, 'contact/about.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context = {'title': 'contact us', 'form': form}
    return render(request, 'contact/contact.html', context)

class UserLogIn(LoginView):
    template_name = 'auth/login.html'
    success_url = ''
    redirect_field_name = settings.REDIRECT_FIELD_NAME

class UserLogOut(LogoutView):
    template_name = 'auth/logout.html'
    url = 'login'

def card(request):
    return render(request, 'product/snippets/card.html')