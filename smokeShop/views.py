from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . models import Product, OrderItem, Order, Payment
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator


from userApps.models import Profile
from . extras import generate_order_id


from paypal.standard.forms import PayPalPaymentsForm
import uuid
from .forms import CheckoutForm



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
  form = CheckoutForm()
  if request.method == 'POST':
      form = CheckoutForm(request.POST)
      if form.is_valid():
          first_name = form.cleaned_data.get('first_name')
          last_name = form.cleaned_data.get('last_name')
          street_address = form.cleaned_data.get('street_address')
          apartment_address = form.cleaned_data.get('apartment_address')
          country = form.cleaned_data.get('country')
          state = form.cleaned_data.get('state')
          city = form.cleaned_data.get('city')
          zip = form.cleaned_data.get('zip')
          same_billing_address = form.cleaned_data.get('same_billing_address')
          save_info = form.cleaned_data.get('save_info')
          if same_billing_address:
              billing_address = street_address
              billing_apartment_address = apartment_address
              billing_country = country
              billing_state = state
              billing_city = city
              billing_zip = zip
          else:
              billing_address = form.cleaned_data.get('billing_address')
              billing_apartment_address = form.cleaned_data.get('billing_apartment_address')
              billing_country = form.cleaned_data.get('billing_country')
              billing_state = form.cleaned_data.get('billing_state')
              billing_city = form.cleaned_data.get('billing_city')
              billing_zip = form.cleaned_data.get('billing_zip')
          order = Order.objects.filter(user=request.user, ordered=False)
          if order.exists():
              order = order[0]
              order.first_name = first_name
              order.last_name = last_name
              order.email = request.user.email
              order.address = street_address
              order.apartment_address = apartment_address
              order.city = city
              order.state = state
              order.country = country
              order.zip = zip
              order.billing_address = billing_address
              order.billing_apartment_address = billing_apartment_address
              order.billing_country = billing_country
              order.billing_state = billing_state
              order.billing_city = billing_city
              order.billing_zip = billing_zip
              order.save()
              return redirect(reverse('payment', kwargs={'pk': order.id}))
          else:
              messages.warning(request, "You do not have an active order")
              return redirect(reverse('cart'))
  return render(request, 'smokeShop/checkout.html', {'form': form})

  



#PAYPAL PAYMENT
def payment(request, pk):
  order = Order.objects.get(id=pk)
  host = request.get_host()
  invoice_number = str(uuid.uuid4())
  paypal_dict = {
      'business': settings.PAYPAL_RECEIVER_EMAIL,
      'amount': order.get_cart_total(),
      'item_name': f'order number {invoice_number}',
      'invoice': invoice_number,
      'currency_code': 'USD',
      'notify_url': f"http://{host}{reverse('paypal-ipn')}",
      'return_url': f"http://{host}{reverse('paypal_return')}",
      'cancel_return': f"http://{host}{reverse('paypal_cancel')}",
  }


  form = PayPalPaymentsForm(initial=paypal_dict)
  context = {'form': form,
             'order': order}
  
  return render(request, 'smokeShop/payPal_Payment.html', context)




#paypal return and cancel
def paypal_return(request):
  return redirect('order_confirmation')

def paypal_cancel(request):
  messages.warning(request, 'Payment was cancelled')
  return redirect('home')

def order_confirmation(request):
  messages.success(request, 'Payment was successful')
  return render(request, 'smokeShop/order_confirmation.html')




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







def blog(request):
  return render(request, 'smokeShop/blog.html')