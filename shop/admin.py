from django.contrib import admin
from .models import Product, Category, ProductGallery
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display= ['name', 'price', 'category', 'stock', 'image']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(ProductGallery)