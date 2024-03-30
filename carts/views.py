from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart

def cart(request,tax=0,grand_total=0,total=0,quantity=0,cart_items=None):
  try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(cart_id=_cart_id(request))

  cart_items=CartItem.objects.filter(cart=cart,is_active=True)
  for i in cart_items:
    total += i.quantity * i.product.price
    quantity += i.quantity
    tax=(total*7.75)/100
    grand_total=tax+total

  
  context={
   'total':total,
   'quantity':quantity,
   'cart_items':cart_items,
   'tax':tax,
   'grand_total':grand_total
  }
  return render(request,'store/cart.html',context)

def remove_cart(request,product_id,cart_item_id):
  #cart = get_object_or_404(Cart,cart_id=_cart_id(request))
  #product = get_object_or_404(Product,id=product_id)
  #cart_item=CartItem.objects.get(product=product,cart=cart)
  cart_item=CartItem.objects.get(id=cart_item_id)
  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()

  return redirect('cart')


def add_cart(request,product_id):
   #get the product
  product = Product.objects.get(id=product_id)
  print(product)
  #variation passed
  product_variations=[]
  if request.method=='POST':
    for item in request.POST:
      key=item
      value=request.POST[key]
      try:
        variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
        product_variations.append(variation)
      except:        
        pass     
      
 
  #get the cart
  try:
    cart=Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    cart = Cart.objects.create(cart_id=_cart_id(request))
  #get the item and update the qty otherwise add the item to cart  
  try:
    cart_items=CartItem.objects.filter(cart=cart,product=product)
    variations = []
    ids=[]
    for i in cart_items:
      variations.append(list(i.variations.all()))
      ids.append(i.id)    
    if(product_variations in variations):
     index=variations.index(product_variations)
     item_id=ids[index]
     item = CartItem.objects.get(product=product_id,id=item_id)
     item.quantity +=1
     item.save()
    else:
      cart_item = CartItem.objects.create(cart=cart,product=product,quantity=1)
      for v in product_variations:
        cart_item.variations.add(v)
      cart_item.save()
  except CartItem.DoesNotExist:
    cart_item = CartItem.objects.create(cart=cart,product=product,quantity=1)
    if len(product_variations) > 0:
      for v in product_variations:
        cart_item.variations.add(v)
    cart_item.save()
  return redirect('cart')











  
    
      
      
      
 
 


def remove_cart_item(request,cart_item_id):
  #cart = get_object_or_404(Cart,cart_id=_cart_id(request))
  #product = get_object_or_404(Product,id=product_id)
  #cart_item = CartItem.objects.get(product=product,cart=cart)
  cart_item=CartItem.objects.get(id=cart_item_id)
  cart_item.delete()

  return redirect('cart')