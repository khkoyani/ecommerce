from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='done'),
    path('api/refresh_cart/', views.api_cart_detail_view, name='refresh-cart'),
]