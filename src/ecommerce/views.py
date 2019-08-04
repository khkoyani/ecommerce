from django.shortcuts import render

def about(request):
    context = {'title': 'about', 'body':'About us'}
    return render(request, 'contact/about.html', context)


def contact(request):
    context = {'title': 'contact us', 'body':'FormControl'}
    return render(request, 'contact/contact.html', context)


