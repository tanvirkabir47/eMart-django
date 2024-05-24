from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.all_product, name='products'),
    path('product/<slug:slug>', views.single_product, name='single-product'),
    path('review/<slug:slug>', views.product_review, name='product-review'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add-to-cart'),
]