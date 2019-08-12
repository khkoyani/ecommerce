from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from carts.models import Cart
from django.http import Http404





class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.get_or_new(self.request)
        context['cart'] = cart_obj
        return context
#     used to find all the variables sent to template

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data( *args, **kwargs)
        cart_obj, new_obj = Cart.objects.get_or_new(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        instance = Product.objects.get_single_object_by_slug(slug)
        return instance

class ProductCreateView(CreateView):
    pass

class ProductUpdateView(UpdateView):
    pass

class ProductDeleteView(DeleteView):
    pass



