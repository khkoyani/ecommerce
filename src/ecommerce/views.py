from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

def about(request):
    context = {'title': 'about', 'body':'About us'}
    return render(request, 'contact/about.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    context = {'title': 'contact us', 'form': form}
    if form.is_valid():
        context['form'] = form
    return render(request, 'contact/contact.html', context)
