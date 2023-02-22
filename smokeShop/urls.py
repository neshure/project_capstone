from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ProductView,
    ProductDetailView,
    DisposableVapeView,
    VapePodsView,
    VapeJuiceView,
    VapeKitView,)



urlpatterns = [
    path('', views.home_age_verify, name='home_age_verify'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<pk>', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user_rating/', views.user_rating, name='user_rating'),
    path('disposable_vape_category/', DisposableVapeView.as_view(), name='disposable_vape_category'),
    path('vape_pods_category/', VapePodsView.as_view(), name='vape_pods_category'),
    path('vape_juice_category/', VapeJuiceView.as_view(), name='vape_juice_category'),
    path('vape_kit_category/', VapeKitView.as_view(), name='vape_kit_category'),
    path('payment/<pk>', views.payment, name='payment'),
    path('paypal_return/', views.paypal_return, name='paypal_return'),
    path('paypal_cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('blog/', views.blog, name='blog'),
]


#This would allow media to work within the browser
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)