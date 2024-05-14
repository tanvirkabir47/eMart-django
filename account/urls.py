from django.urls import path
from . import views

urlpatterns = [
    path('account/login/', views.login_view, name = 'login'),
    path('account/create-account/', views.signup_view, name = 'signup'),
    path('logout/', views.logout_views, name = 'logout'),
    path('account/forgot-password/', views.forgot_password, name = 'forgot-password'),
    path('resetpassword_validate/<uidb64>/<token>/<time64>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]