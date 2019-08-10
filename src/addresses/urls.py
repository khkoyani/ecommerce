from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.address_create_view, name='create'),
    path('saved', views.use_saved_address_view, name='saved_addresses'),
]