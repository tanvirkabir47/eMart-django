from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Cart, Product, Category, ProductReview

# Create your views here.

def home(request):
    products = Product.objects.all()
    feature_products = Product.objects.filter(is_feature = True)
    return render(request, 'index.html', {'products': products, 'feature_products': feature_products})

def all_product(request):
    products = Product.objects.all()
    return render(request, 'shop-category.html', {'products': products})

def single_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'single-product.html', {'product': product})

def product_review(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        review_message = request.POST.get('review_message')
        rating = request.POST.get('rating')
        
        if not rating:
            rating = 1.0
            
        review = ProductReview(
            product=product,
            user=request.user,
            subject=subject,
            review_message=review_message,
            rating=rating
        )
        review.save()
        return redirect(reverse('single-product', kwargs={'slug': slug}))
    


def add_to_cart(request, id):
    
    if request.user.is_authenticated:
        user = request.user
        product = get_object_or_404(Product, pk=id)
        quantity = request.POST.get('quantity')
        
        if quantity:
            quantity = int(quantity),
        else:
            quantity = 1
        
        cart = Cart(
            user = user, 
            product = product,
            quantity = quantity,
        )
         
        cart.save()
        
        return redirect('home')
    
    else:
        return redirect('/account/login')
    
    

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')