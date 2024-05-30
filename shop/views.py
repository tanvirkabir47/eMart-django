from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Cart, Product, Category, ProductReview, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

# Create your views here.

def home(request):
    products = Product.objects.all()
    feature_products = Product.objects.filter(is_feature = True)
    return render(request, 'index.html', {'products': products, 'feature_products': feature_products})

def all_product(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('product'))
    return render(request, 'shop-category.html', {'products': products, 'categories': categories})

def categories_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category__slug=slug)
    categories = Category.objects.annotate(product_count=Count('product'))
    
    return render(request, 'shop-category-data.html', {'products': products, 'category': category, 'categories': categories})

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
            
        if Cart.objects.filter(user=user, product=product).exists():
            messages.error(request, 'Product is already exists')
        else:
            cart = Cart(
                user = user, 
                product = product,
                quantity = quantity,
            )
         
            cart.save()
            messages.success(request, "Cart Item added successfully!!!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    else:
        return redirect('/account/login')
    


@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        if request.user.is_authenticated:
            user = request.user
            cart_item = Cart.objects.get(user=user, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()

            # Calculate the updated prices
            updated_price = float(cart_item.product.price * cart_item.quantity)
            cart_items = Cart.objects.filter(user=user)
            cart_subtotal = sum(item.product.price * item.quantity for item in cart_items)
            shipping_cost = 50  # Shipping cost is $10
            discount = cart_subtotal * Decimal(0.05)
            cart_total = cart_subtotal + shipping_cost - discount

            return JsonResponse({
                'cart_total': float(cart_total),
                'cart_subtotal': float(cart_subtotal),
                'shipping_cost': float(shipping_cost),
                'updated_price': updated_price,
                'product_id': product_id,
            })
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def remove_from_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        cart = get_object_or_404(Cart, id=id, user=user)
        cart.delete()
        messages.success(request, "Cart Item remove successfully!!!")
        return redirect('add-cart-view') 
    
    else:
        return redirect('/account/login')
    
    
    
def cart(request):
    return render(request, 'cart-page.html',)


@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})


def add_to_fav(request, id):
    if request.user.is_authenticated:
        user = request.user
        product = get_object_or_404(Product, pk=id)
        
        
        if Wishlist.objects.filter(user=user, product=product).exists():
            messages.error(request, "Product is already in your wishlist.")
        else:
            wishlist = Wishlist(user=user, product=product)
            wishlist.save()
            messages.success(request, "Wishlist item added successfully!")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    else:
        return redirect('/account/login')
    
@login_required
def remove_from_fav(request, id):
    if request.user.is_authenticated:
        user = request.user
        wishlist = get_object_or_404(Wishlist, id=id, user=user)
        wishlist.delete()
        messages.success(request, "Wishlist Item remove successfully!!!")
        print(wishlist)
        return redirect('wishlist')
    


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')