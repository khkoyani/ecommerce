from django.urls import path
from . import views

urlpatterns = [
    path('<slug>/detail/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),

]
