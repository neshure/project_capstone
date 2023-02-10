import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from . models import Product
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.views import View
from django.http import HttpResponse, JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
  return render(request, 'smokeShop/home.html')

def about(request):
  return render(request, 'smokeShop/about.html')

def cart(request):
  return render(request, 'smokeShop/cart.html')

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

class CheckoutView(View):
  def get(self, *args, **kwargs):
    product = Product.objects.get(id=self.kwargs['pk'])
    context = super().get_context_data(**kwargs)
    context.update({
      'product': product,
    })
    return render(self.request, 'smokeShop/checkout.html', context)

class CreateCheckoutSessionView(View):
  def post(self, request, *args, **kwargs):
    product_id = self.kwargs['pk']
    product = Product.objects.get(id=product_id)
    YOUR_DOMAIN = 'http://127.0.0.1:8000'
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {

              'price_data': {
                'currency': 'usd',
                'unit_amount': int(product.price * 100  ),
                'product_data': {
                  'name': product.title,
                },
              },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    return JsonResponse({'id': checkout_session.id})

# if __name__ == '__main__':
#     app.run(port=4242)







