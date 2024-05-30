from django.db import models
from autoslug import AutoSlugField

from account.models import User

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
    stock = models.IntegerField()
    is_feature = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created_at',)
        
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
    
    def review_count(self):
        return self.reviews.count()
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    product_gallery = models.ImageField(upload_to='products_images/products_images_gallery/')
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = 'Product Galleries'
        
        
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='customers', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    review_message = models.TextField()
    rating = models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name    
    
    class Meta:
        ordering = ('-created_at',)
        
        
class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        ordering = ('-created_at',)
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        ordering = ('-created_at',)