from django import forms
from .models import Product, Payment






#User rating form
class UserRatingForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['rating', 'user_review']


class PaymentForm(forms.ModelForm):
  class Meta:
    model = Payment
    fields = ['currency', 'description']
