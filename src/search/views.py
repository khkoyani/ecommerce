from django.shortcuts import render
from product.models import Product
from django.views.generic import ListView

class SearchProductView(ListView):
    model = Product
    template_name = 'search/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        print(context)
        return context



    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        print(query)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.none()
# Create your views here.
