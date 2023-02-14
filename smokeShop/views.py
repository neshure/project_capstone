import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . models import Product, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views import View
from django.http import HttpResponse, JsonResponse
from userApps.models import Profile
from . extras import generate_order_id
from django.db.models import Avg
from .forms import UserRatingForm




def home(request):
  return render(request, 'smokeShop/home.html')

def about(request):
  return render(request, 'smokeShop/about.html')



@login_required
def add_to_cart(request, **kwargs):
  # get the user's profile
  user_profile = get_object_or_404(Profile, user=request.user)
  # filter products by id
  id=int(kwargs.get('pk'))
  product = Product.objects.get(id=id)
  # create orderItem of the selected product
  order_item, status_ = OrderItem.objects.get_or_create(product=product)
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



def user_rating(request):
  return render(request, 'smokeShop/user_rating.html')




