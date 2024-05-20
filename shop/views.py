from django.shortcuts import get_object_or_404, render
from .models import Product, Category

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def all_product(request):
    products = Product.objects.all()
    return render(request, 'shop-category.html', {'products': products})

def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'single-product.html', {'product': product})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')