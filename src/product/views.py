from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product





class ProductListView(ListView):
    model = Product

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
#     used to find all the variables sent to template

class ProductDetailView(DetailView):
    model = Product

class ProductCreateView(CreateView):
    pass

class ProductUpdateView(UpdateView):
    pass

class ProductDeleteView(DeleteView):
    pass



