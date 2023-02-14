from django import forms
from .models import Product





#User rating form
class UserRatingForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['rating', 'user_review']