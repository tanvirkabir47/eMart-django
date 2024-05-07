from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def all_product(request):
    return render(request, 'shop-category.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')