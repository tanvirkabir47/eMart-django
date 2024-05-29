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
    path('remove-from-cart/<int:id>', views.remove_from_cart, name='remove-from-cart'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update-cart-quantity'),
    path('all-cart-view/', views.cart, name='add-cart-view'),
]