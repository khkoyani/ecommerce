from django.shortcuts import render


def home(request):
    context = {
        'content': 'content'
    }
    return render(request, 'ecommerce/home.html', context)
# Create your views here.
