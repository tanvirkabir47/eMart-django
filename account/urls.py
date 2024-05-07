from django.urls import path
from . import views

urlpatterns = [
    path('account/login', views.login_view, name = 'login')
]