from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/guest/', views.guest_login_view, name='guest_login')
    # path('logout/', views.log_out, name='logout'),

]
