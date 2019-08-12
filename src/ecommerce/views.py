from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
        print(form.cleaned_data)
        context['form'] = form
        if request.is_ajax():
            return JsonResponse({'message': 'Form Submitted Successfully'})
    if form.errors:
        print('error')
        print(form.errors)
        errors = form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, 'contact/contact.html', context)
