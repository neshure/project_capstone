from django.contrib import admin
from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', user_views.signup, name='account_signup'),
    path('login/', user_views.login, name='account_login'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userApps/logout.html'), name='account_logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='userApps/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='userApps/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='userApps/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='userApps/password_reset_complete.html'), name='password_reset_complete'),
]