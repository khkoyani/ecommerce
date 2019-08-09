from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_page, name='login'),
    # path('logout/', views.log_out, name='logout'),

]