from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    ProductView,
    ProductDetailView,)



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<pk>', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/', ProductView.as_view(), name='product'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('user_rating/', views.user_rating, name='user_rating'),
]


#This would allow media to work within the browser
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)