from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category

from .models import Product

from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request,category_slug=None):
  category=None
  products=None
  if category_slug != None:
    category=get_object_or_404(Category,slug=category_slug)
    products=Product.objects.filter(category=category,is_available=True).order_by('id')
    paginator = Paginator(products,2)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
  else:
    products=Product.objects.filter(is_available=True).order_by('id')
    paginator = Paginator(products,2)
    page = request.GET.get('page')
    paged_products=paginator.get_page(page)
    product_count=products.count()
    
  context={"products":paged_products,"product_count":product_count}
  return render(request,"store/store.html",context)

def product_detail(request,category_slug,product_slug):
  try:
    single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
  except Exception as e:
    raise e
  
  context = {
    'single_product':single_product,
    'in_cart':in_cart,
  }
  return render(request,'store/product_detail.html',context)

def search(request):
  keyword=""
  products=None
  if 'keyword' in request:
    keyword=request.GET['keyword']

  if keyword:
    products = Product.objects.filter(description__icontains=keyword)

  context={'products':products}
  return render(request,'store/store.html',context)