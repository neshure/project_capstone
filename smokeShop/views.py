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
  messages.info(request, "item added to cart")
  return redirect(reverse('product'))


@login_required
def cart(request):
  order = Order.objects.filter(user=request.user, ordered=False)
  if order.exists():
      order = order[0]
      return render(request, 'smokeShop/cart.html', {'order': order})
  
  


def remove_from_cart(request, **kwargs):
  item_to_delete = OrderItem.objects.filter(pk=kwargs.get('item_id', ""))
  if item_to_delete.exists():
      item_to_delete[0].delete()
      messages.info(request, "Item has been deleted")
  return redirect(reverse('product_detail'))






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

class SuccessView(View):
  def get(self, *args, **kwargs):
    return render(self.request, 'smokeShop/success.html', {})

class CancelledView(View):
  def get(self, *args, **kwargs):
    return render(self.request, 'smokeShop/cancel.html', {})

# class CheckoutView(View):
#   def get(self, *args, **kwargs):
#     print(kwargs)
#     product_id = self.kwargs['pk']
#     context = super().get_context_data(**kwargs)
#     context.update({
#       'product': product,
#     })
#     return render(self.request, 'smokeShop/checkout.html', context)

# class CreateCheckoutSessionView(View):
#   def post(self, request, *args, **kwargs):
#     product_id = self.kwargs['pk']
#     product = Product.objects.get(id=product_id)
#     YOUR_DOMAIN = 'http://127.0.0.1:8000'
#     checkout_session = stripe.checkout.Session.create(
#         line_items=[
#             {

#               'price_data': {
#                 'currency': 'usd',
#                 'unit_amount': int(product.price * 100  ),
#                 'product_data': {
#                   'name': product.title,
#                 },
#               },
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url=YOUR_DOMAIN + '/success/',
#         cancel_url=YOUR_DOMAIN + '/cancel/',
#     )
#     return JsonResponse({'id': checkout_session.id})

# # if __name__ == '__main__':
# #     app.run(port=4242)







