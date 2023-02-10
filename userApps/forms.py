from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserLoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  #Model form interacts with
  class Meta:
    model = User
  #Fields that's going to be shown
    fields = ['username', 'email', 'password1', 'password2']


#Create a class that will update user model
#Allows user to update email and username
class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField()

  #Model form interacts with
  class Meta:
    model = User
    fields = ['username', 'email']

#Allows user to update image
class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = []