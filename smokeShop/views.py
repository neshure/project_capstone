import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, OrderItem, Order, Payment
from payments import get_payment_model, RedirectNeeded
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from userApps.models import Profile
from . extras import generate_order_id
from django.db.models import Avg
from .forms import UserRatingForm
from decimal import Decimal

from payments import get_payment_model



def home_age_verify(request):
  return render(request, 'smokeShop/home_age_verify.html')

def home(request):
  return render(request, 'smokeShop/home.html')

def about(request):
  return render(request, 'smokeShop/about.html')



@login_required
def add_to_cart(request, **kwargs):
  quantity = request.POST.get('quantity-form', 1)
  # get the user's profile
  user_profile = get_object_or_404(Profile, user=request.user)
  # filter products by id
  id=int(kwargs.get('pk'))
  product = Product.objects.get(id=id)
  # create orderItem of the selected product
  order_item, status_ = OrderItem.objects.get_or_create(product=product)
  order_item.quantity = quantity
  order_item.save()
  # create order associated with the user
  user_order, status_ = Order.objects.get_or_create(user=user_profile.user, ordered=False)
  user_order.order_item.add(order_item)
  # generate a reference code
  user_order.ref_code = generate_order_id()
  user_order.save()
    # show confirmation message and redirect back to the same page
  return redirect(reverse('product'))
  



@login_required
def cart(request):
  order = Order.objects.filter(user=request.user, ordered=False)
  if order.exists():
      order = order[0]
      return render(request, 'smokeShop/cart.html', {'order': order})
  else:
      return render(request, 'smokeShop/cart.html', {'order': order})
  
  


# remove product from cart

@login_required
def remove_from_cart(request, **kwargs):
  if request.method == 'POST':
      id = int(kwargs.get('pk'))
      order_item = OrderItem.objects.get(id=id)
      order = Order.objects.filter(user=request.user, ordered=False)
      if order.exists():
          order = order[0]
          order.order_item.remove(order_item)
          return redirect(reverse('cart'))
      else:
          return redirect(reverse('cart'))






def checkout(request):
  return render(request, 'smokeShop/checkout.html')


class ProductView(ListView):
  model = Product
  template_name = 'smokeShop/product.html'
  context_object_name = 'products' #Tells ListView what variable to loop over in the template
  paginate_by = 15


class ProductDetailView(DetailView):
  model = Product
  template_name = 'smokeShop/product_detail.html'
  context_object_name = 'product'



class VapePodsView(ListView):
  model = Product
  template_name = 'smokeShop/vape_pods_category.html'
  context_object_name = 'vape_pods_products' #Tells ListView what variable to loop over in the template
  paginate_by = 15

  def get_queryset(self):
    return Product.objects.filter(category='Vape Pods')


class VapeKitView(ListView):
  model = Product
  template_name = 'smokeShop/vape_kits_category.html'
  context_object_name = 'vape_kit_products' #Tells ListView what variable to loop over in the template
  paginate_by = 15

  def get_queryset(self):
    return Product.objects.filter(category='Vape Kits')




class VapeJuiceView(ListView):
  model = Product
  template_name = 'smokeShop/vape_juice_category.html'
  context_object_name = 'vape_juice_products' #Tells ListView what variable to loop over in the template
  paginate_by = 15

  def get_queryset(self):
    return Product.objects.filter(category='vape juice')




class DisposableVapeView(ListView):
  model = Product
  template_name = 'smokeShop/disposable_vape_category.html'
  context_object_name = 'disposable_vape_products' #Tells ListView what variable to loop over in the template
  paginate_by = 15
  
  def get_queryset(self):
    return Product.objects.filter(category='Disposable Vapes')



def user_rating(request):
  return render(request, 'smokeShop/user_rating.html')




# payment gateway
def payment_details(request, payment_id):
  payment = get_object_or_404(Payment, id=payment_id)
  try:
    form = payment.get_form(data=request.POST or None)
  except RedirectNeeded as redirect_to:
    return redirect(redirect_to)
  return render(request, 'smokeShop/payment_details.html', {'payment': payment, 'form': form})


# payment process
def payment(request):
  order_id = request.session.get('order_id')
  order = get_object_or_404(Order, id=order_id)

  payment = get_payment_model().objects.create(
    variant='default',
    description=order_id,
    total=order.get_total(),
    currency='USD',
    delivery=order.get_total(),
    billing_first_name=order.user.first_name,
    billing_last_name=order.user.last_name, 
    customer_ip_address='127.0.0.1',)
  request.session['payment_id'] = payment.id
  return render(request, 'smokeShop/payment.html', {'payment': payment})


