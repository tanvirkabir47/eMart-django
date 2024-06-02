from .models import Cart, Category
from decimal import Decimal

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user = user)
        
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
        
        cart_subtotal = sum(item.total_price for item in cart_items)
        shipping_cost = 50
        discount = cart_subtotal * Decimal(0.05)
        cart_total = cart_subtotal + shipping_cost - discount
    else:
        cart_items = []
        cart_total = 0
        cart_subtotal = 0
        shipping_cost = 0
        
    return {
        'cart_items': cart_items, 
        'cart_total': cart_total, 
        'cart_subtotal': cart_subtotal,
        'shipping_cost': shipping_cost,
    }
    
def categories(request):
    categories = Category.objects.all()
    
    return {
        'categories': categories,
    }