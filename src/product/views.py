from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product

def home(request):
    context = {
        'content': 'content'
    }
    return render(request, 'product/home.html', context)



class ProductListView(ListView):
    model = Product

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
#     used to find all the variables sent to template

