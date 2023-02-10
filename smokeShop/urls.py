from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductView
from .views import CreateCheckoutSessionView, CheckoutView, SuccessView, CancelledView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('cancel/', CancelledView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('product/', ProductView.as_view(), name='product'),
]


#This would allow media to work within the browser
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)