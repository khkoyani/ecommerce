from django.shortcuts import render
from product.models import Product
from django.views.generic import ListView
from django.db.models import Q

class SearchProductView(ListView):
    model = Product
    template_name = 'search/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        print(f'context = {context}')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()
# Create your views here.
