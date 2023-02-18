from django import forms
from .models import Product
import datetime






#User rating form
class UserRatingForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['rating', 'user_review']


class CheckoutForm(forms.Form):
  first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
  last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
  street_address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': '1234 Main St'
  }))
  apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
    'placeholder': 'Apartment or suite'
  }))
  country = forms.CharField( widget=forms.TextInput(attrs={
    'placeholder': 'Country'
  }))
  state = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'State'
  }))
  city = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'City'
  }))
  zip = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Zip'
  }))
  same_billing_address = forms.BooleanField(required=False)
  save_info = forms.BooleanField(required=False)
  payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=[
    ('S', 'Stripe'),
    ('P', 'PayPal')
  ])
  billing_address = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  billing_apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  billing_country = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  billing_state = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  billing_city = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  billing_zip = forms.CharField(required=False, widget=forms.TextInput(attrs={}))
  
  
  def clean(self):
    data = self.cleaned_data
    if data.get('same_billing_address'):
      data['billing_address'] = data.get('street_address')
      data['billing_apartment_address'] = data.get('apartment_address')
      data['billing_country'] = data.get('country')
      data['billing_state'] = data.get('state')
      data['billing_city'] = data.get('city')
      data['billing_zip'] = data.get('zip')
    return data
  
  def clean_zip(self):
    zip = self.cleaned_data.get('zip')
    if len(zip) < 5:
      raise forms.ValidationError('Zip code must be 5 digits')
    return zip  
  
 
  
  def clean_street_address(self):
    street_address = self.cleaned_data.get('street_address')
    if len(street_address) < 5:
      raise forms.ValidationError('Address must be 5 characters or more')
    return street_address
  
  def clean_country(self):
    country = self.cleaned_data.get('country')
    if len(country) < 2:
      raise forms.ValidationError('Country must be 2 characters or more')
    return country
  
  def clean_state(self):
    state = self.cleaned_data.get('state')
    if len(state) < 2:
      raise forms.ValidationError('State must be 2 characters or more')
    return state
  
  def clean_city(self):
    city = self.cleaned_data.get('city')
    if len(city) < 2:
      raise forms.ValidationError('City must be 2 characters or more')
    return city
  
  def clean_full_name(self):
    full_name = self.cleaned_data.get('full_name')
    if len(full_name) < 2:
      raise forms.ValidationError('Full name must be 2 characters or more')
    return full_name
  
  def clean_payment_option(self):
    payment_option = self.cleaned_data.get('payment_option')
    if payment_option == 'S':
      raise forms.ValidationError('Stripe is not yet supported')
    return payment_option
  
  