from carts.models import Cart, CartItem
from carts.views import _cart_id


def counter(request):
  cart_count=0
  if 'admin' in request.path:
    return {}
  else:
    try:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartItem.objects.all().filter(cart=cart)
      for i in cart_items:
        cart_count += i.quantity
    except Cart.DoesNotExist:
      cart_count=0
  
  return dict(cart_count=cart_count)