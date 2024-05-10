from datetime import timezone
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='profile/', default='../static/assets/img/clients/logo-02.png')
    phone=models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=50,blank=True)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50,blank=True)
    state = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return self.username
    