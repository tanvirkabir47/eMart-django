from django.contrib import admin
from .models import Product, Category, ProductReview, Cart
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display= ['name', 'price', 'category', 'stock', 'image']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['name']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display= ['product', 'user', 'rating']
    
class CartAdmin(admin.ModelAdmin):
    list_display= ['product', 'user', 'quantity']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Cart, CartAdmin)

