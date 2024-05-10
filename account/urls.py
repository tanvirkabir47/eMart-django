from django.urls import path
from . import views

urlpatterns = [
    path('account/login/', views.login_view, name = 'login'),
    path('account/create-account/', views.signup_view, name = 'signup'),
    path('logout/', views.logout_views, name = 'logout'),
]