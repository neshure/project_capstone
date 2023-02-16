from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as user_login, logout as user_logout



def login(request):
    if request.method == 'GET':
        form = UserLoginForm()
    else:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                user_login(request, user)
                previous_page = request.GET.get('next')
                if previous_page is not None:
                    return redirect(previous_page)
                else:
                    return redirect('home')
    return render(request, 'userApps/login.html', {'form': form})


def logout(request):
    user_logout(request)
    return redirect('home')


def signup(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f"Account created for {username}!")
        user_login(request, user)
        return redirect('home')
    else:
        messages.error(request, "There was an error creating your account.")
    return render(request, 'userApps/signup.html', {'form': form})






#Create a page for Users profile

@login_required #adds functionality to profile view. User must be logged in to view page
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userApps/profile.html', context)


