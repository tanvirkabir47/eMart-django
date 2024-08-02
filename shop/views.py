import stripe
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Cart, Product, Category, ProductReview, Wishlist, Order
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.core.paginator import Paginator
from django.conf import settings

# Create your views here.

def home(request):
    products = Product.objects.all()
    feature_products = Product.objects.filter(is_feature = True)
    return render(request, 'index.html', {'products': products, 'feature_products': feature_products})

def all_product(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('product'))
    paginator = Paginator(products, 3)
    
    page = request.GET.get('page', 1)
    paginates = paginator.page(page)
    return render(request, 'shop-category.html', {'categories': categories, 'paginates': paginates,})

def categories_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category__slug=slug)
    categories = Category.objects.annotate(product_count=Count('product'))
    
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paginates = paginator.get_page(page_number)
    
    return render(request, 'shop-category-data.html', {
        'products': products, 
        'category': category, 
        'categories': categories,
        'paginates': paginates,
        'show_pagination': paginator.count > 6
    })

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


def search(request):
    query = request.POST.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
        
    product_count = products.count()
    paginator = Paginator(products, 8)
    
    page = request.GET.get('page', 1)
    paginates = paginator.get_page(page)
    
    return render(request, 'search.html', {
        'products': products,
        'query': query, 
        'paginates': paginates,
        'show_pagination': product_count > 8
    })
    
    
@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    cart_item_details = []
    cart_subtotal = 0
    for item in cart_items:
        total_price = item.product.price * item.quantity
        cart_subtotal += total_price
        cart_item_details.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': total_price
        })

    shipping_cost = 50
    discount = cart_subtotal * Decimal(0.05)
    cart_total = cart_subtotal + shipping_cost - discount
    amount_in_cents = int(cart_total * 100)

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if not all([first_name, last_name, email, address, phone, city, postal_code, state, country]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('checkout')

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            charge = stripe.Charge.create(
                amount=amount_in_cents,  # Stripe expects the amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )

            # Create order and save to database
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                phone=phone,
                city=city,
                postal_code=postal_code,
                state=state,
                country=country,
                total_price=cart_total
            )

            # Once payment is successful, clear the cart and show success message
            cart_items.delete()
            messages.success(request, "Thank you for your order!")
            return redirect('home')

        except stripe.error.CardError as e:
            messages.error(request, "Your card has been declined.")

    return render(request, 'checkout.html', {
        'cart_item': cart_item_details,
        'cart_total': cart_total,
        'amount_in_cents': amount_in_cents,
        'cart_subtotal': cart_subtotal,
        'shipping_cost': shipping_cost,
        'discount': discount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })