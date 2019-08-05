from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from django.http import Http404





class ProductListView(ListView):
    model = Product

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
#     used to find all the variables sent to template


class ProductDetailView(DetailView):
    model = Product

    def get_object(self,  *args, **kwargs ):
        request = self.request
        # gets the current request
        slug = self.kwargs.get('slug')
        # all parameters sent as part of the url are stored in kwargs
        instance = Product.objects.get_by_slug(slug=slug)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance

class ProductCreateView(CreateView):
    pass

class ProductUpdateView(UpdateView):
    pass

class ProductDeleteView(DeleteView):
    pass



