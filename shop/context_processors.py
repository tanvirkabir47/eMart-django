from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user = user)
        cart_total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        cart_total= []
        
    return {'cart_items': cart_items, 'cart_total': cart_total}