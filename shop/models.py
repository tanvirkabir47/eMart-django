from django.db import models
from autoslug import AutoSlugField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
  


class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='products_images/')
    quick_overview = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.FloatField()
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created_at',)
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    product_gallery = models.ImageField(upload_to='products_images/products_images_gallery/')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Product Galleries'
    