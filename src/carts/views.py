from django.shortcuts import render

def cart_home(request):

    key= request.session.session_key
    request.session['first_name'] = 'Karan'
    return render(request, 'carts/home.html', {})
# Create your views here.
